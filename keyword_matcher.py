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

    for _, row in db.iterrows():

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

        # -------------------
        # 핵심 검색어 묶기
        # -------------------
        search_terms = (
            [keyword]
            + aliases
            + pronunciation
        )

        # -------------------
        # 연관 텍스트
        # -------------------
        related_text = " ".join([
            description,
            clinical_feature,
            related_disease,
            related_assessment,
            related_special_test,
            related_exercise
        ])

        # -------------------
        # 정확 keyword 검색
        # -------------------
        if query == keyword:

            row_dict = row.to_dict()

            row_dict["_score"] = 9999

            results.append(
                row_dict
            )

            continue

        # -------------------
        # 핵심 단어 점수
        # -------------------
        matched_terms = 0

        for term in search_terms:

            term = (
                str(term)
                .strip()
                .lower()
            )

            if (
                not term
                or len(term) < 2
            ):
                continue

            # 정확 포함
            if term in query:

                score += 100
                matched_terms += 1

            # 띄어쓰기 대응
            elif any(
                term in w
                for w in words
            ):

                score += 70
                matched_terms += 1

            # 오타 허용
            else:

                sim = similarity(
                    term,
                    query
                )

                if sim >= 0.85:

                    score += 40
                    matched_terms += 1

        # -------------------
        # 설명 기반 관련도
        # -------------------
        for word in words:

            if len(word) < 2:
                continue

            # 검사명 / 질환명은 강하게
            if (
                word in related_special_test
                or word in related_assessment
                or word in related_disease
            ):

                score += 30

            # 설명은 약하게
            elif (
                word in description
                or word in clinical_feature
            ):

                score += 10

        # -------------------
        # 관련 카드 강화
        # -------------------
        if matched_terms >= 1:

            if keyword in related_text:

                score += 25

        # -------------------
        # 최소 점수 제한
        # -------------------
        if score >= 60:

            row_dict = (
                row.to_dict()
            )

            row_dict[
                "_score"
            ] = score

            results.append(
                row_dict
            )

    # -------------------
    # 중복 제거
    # -------------------
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

    return results[:7]