def find_keywords(
    query,
    db
):

    query = str(
        query
    ).lower().strip()

    words = query.split()

    results = []

    for _, row in db.iterrows():

        score = 0

        keyword = str(
            row.get(
                "keyword",
                ""
            )
        ).lower()

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

        search_terms = [
            keyword
        ] + aliases + pronunciation

        for term in search_terms:

            term = (
                term
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
            elif term in query:
                score += 10

        if score >= 30:

            row_dict = (
                row.to_dict()
            )

            row_dict[
                "_score"
            ] = score

            results.append(
                row_dict
            )

    # 점수순 정렬
    results = sorted(
        results,
        key=lambda x:
        x["_score"],
        reverse=True
    )

    return results[:5]