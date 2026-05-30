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

    words = (
        query.split()
    )

    results = []

    for _, row in (
        db.iterrows()
    ):

        score = 0

        keyword = str(
            row.get(
                "keyword",
                ""
            )
        ).lower().strip()

        aliases = str(
            row.get(
                "aliases",
                ""
            )
        ).lower().split(",")

        pronunciation = str(
            row.get(
                "pronunciation",
                ""
            )
        ).lower().split(",")

        search_terms = (
            [keyword]
            + aliases
            + pronunciation
        )

        # 정확 keyword 우선
        if query == keyword:

            row_dict = (
                row.to_dict()
            )

            row_dict[
                "_score"
            ] = 9999

            results.append(
                row_dict
            )

            continue

        # 검색 점수 계산
        for term in (
            search_terms
        ):

            term = (
                str(term)
                .strip()
            )

            if not term:
                continue

            # 완전 일치
            if term == query:

                score += 100

            # 단어 일치
            elif term in words:

                score += 50

            # 부분 일치
            elif (
                term in query
                and len(term) >= 2
            ):

                score += 10

        if score >= 20:

            row_dict = (
                row.to_dict()
            )

            row_dict[
                "_score"
            ] = score

            results.append(
                row_dict
            )

    results = sorted(
        results,
        key=lambda x:
        x["_score"],
        reverse=True
    )

    return results[:10]
