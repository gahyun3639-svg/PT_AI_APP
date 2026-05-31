from difflib import SequenceMatcher


# -------------------
# 유사도
# -------------------
def similarity(a, b):

    return SequenceMatcher(
        None,
        a,
        b
    ).ratio()


# -------------------
# 핵심 검색 엔진
# -------------------
def find_keywords(query, db):

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

        description = str(
            row.get(
                "description",
                ""
            )
        ).lower()

        clinical_feature = str(
            row.get(
                "clinical_feature",
                ""
            )
        ).lower()

        related_disease = str(
            row.get(
                "related_disease",
                ""
            )
        ).lower()

        related_assessment = str(
            row.get(
                "related_assessment",
                ""
            )
        ).lower()

        related_special_test = str(
            row.get(
                "related_special_test",
                ""
            )
        ).lower()

        related_exercise = str(
            row.get(
                "related_exercise",
                ""
            )
        ).lower()

        search_terms = (
            [keyword]
            + aliases
            + pronunciation
        )

        related_text = " ".join([
            description,
            clinical_feature,
            related_disease,
            related_assessment,
            related_special_test,
            related_exercise
        ])

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

        # -------------------
        # 검색 점수 계산
        # -------------------
        for term in search_terms:

            term = (
                str(term)
                .strip()
                .lower()
            )

            if not term:
                continue

            # 완전 일치
            if term == query:

                score += 100

            # 문장 안 포함
            elif term in query:

                score += 60

            # 단어 일부 포함
            elif any(
                term in w
                for w in words
            ):

                score += 40

            # 설명/질환/검사 관련성
            elif term in related_text:

                score += 15

            # 오타 대응
            else:

                sim = similarity(
                    term,
                    query
                )

                if sim >= 0.75:

                    score += 20

        # -------------------
        # 설명 기반 문장 검색
        # -------------------
        for word in words:

            if len(word) < 2:
                continue

            if word in related_text:

                score += 10

        # 결과 추가
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

    # 중복 제거
    unique_results = {}

    for item in results:

        key = item.get(
            "keyword",
            ""
        )

        if (
            key not in unique_results
            or item["_score"]
            >
            unique_results[key]["_score"]
        ):

            unique_results[
                key
            ] = item

    results = sorted(
        unique_results.values(),
        key=lambda x:
        x["_score"],
        reverse=True
    )

    return results[:10]
