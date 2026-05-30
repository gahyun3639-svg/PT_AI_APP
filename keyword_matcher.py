from difflib import (
    SequenceMatcher
)


# -------------------
# 유사도
# -------------------
def similarity(
    a,
    b
):

    return (
        SequenceMatcher(
            None,
            a,
            b
        ).ratio()
    )


# -------------------
# 핵심 검색 엔진
# -------------------
def find_keywords(
    query,
    db
):

    query = str(
        query
    ).lower().strip()

    query_nospace = (
        query.replace(
            " ",
            ""
        )
    )

    results = []

    # -------------------
    # 의미 키워드
    # -------------------
    semantic_keywords = {

        "mmt": [

            "근력",
            "맨손",
            "도수",
            "힘검사",
            "근력검사"
        ],

        "mas": [

            "강직",
            "경직",
            "근긴장도",
            "긴장도"
        ],

        "rom": [

            "가동범위",
            "관절범위",
            "움직임범위"
        ],

        "acl": [

            "앞십자인대",
            "전방십자인대",
            "무릎앞"
        ],

        "stroke": [

            "중풍",
            "편마비",
            "뇌혈관"
        ],

        "frozen shoulder": [

            "오십견",
            "동결견",
            "유착성"
        ]
    }

    for _, row in db.iterrows():

        score = 0

        keyword = str(
            row.get(
                "keyword",
                ""
            )
        ).lower()

        # -------------------
        # 검색어 수집
        # -------------------
        search_terms = []

        for col in [

            "keyword",
            "aliases",
            "pronunciation",
            "new_term",
            "old_term",
            "english"

        ]:

            value = str(
                row.get(
                    col,
                    ""
                )
            )

            if value:

                terms = [

                    x.strip().lower()

                    for x in value.split(",")

                    if x.strip()
                ]

                search_terms.extend(
                    terms
                )

        search_terms = list(
            set(search_terms)
        )

        # -------------------
        # exact
        # -------------------
        for term in search_terms:

            term_nospace = (
                term.replace(
                    " ",
                    ""
                )
            )

            # 완전일치
            if (
                query == term
            ):

                score += 100

            # 띄어쓰기 무시
            elif (
                query_nospace
                ==
                term_nospace
            ):

                score += 95

            # 정확 keyword 최우선
            if query == keyword:

                score += 1000

            # 완전 일치
            elif term == query:

                score += 100

            # 단어 일치
            elif term in words:

                score += 50

            # 부분 일치
            elif (
                term in query
                and len(term) >= 3
            ):

                score += 5

            # fuzzy
            else:

                sim = similarity(
                    query_nospace,
                    term_nospace
                )

                if sim >= 0.82:
                    score += 40

        # -------------------
        # 의미 추론
        # -------------------
        for key, words in (
            semantic_keywords
            .items()
        ):

            if any(
                word in query
                for word in words
            ):

                if (
                    key
                    in keyword
                ):

                    score += 60

        # -------------------
        # 결과 추가
        # -------------------
        if score >= 35:

            row_dict = (
                row.to_dict()
            )

            row_dict[
                "_score"
            ] = score

            results.append(
                row_dict
            )

    # 정렬
    results = sorted(
        results,
        key=lambda x:
        x["_score"],
        reverse=True
    )

    # 중복 제거
    unique = []
    seen = set()

    for r in results:

        key = str(
            r.get(
                "keyword",
                ""
            )
        )

        if key not in seen:

            unique.append(r)
            seen.add(key)
            # -------------------
            # keyword 정확 매칭 우선
            # -------------------
            final_results = []

            for result in unique:

                keyword = str(
                    result.get(
                        "keyword",
                        ""
                    )
                ).lower()

                if (
                    keyword
                    in query.lower()
                ):

                    final_results.insert(
                        0,
                        result
                    )

                else:

                    final_results.append(
                        result
                    )

            return final_results[:5]

    return unique[:5]