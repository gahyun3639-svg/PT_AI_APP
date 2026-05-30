import pandas as pd


def load_database():

    try:

        db = pd.read_csv(
            "physio_db.csv",
            encoding="utf-8",
            on_bad_lines="skip"
        )

        db = db.fillna("")

        return db

    except Exception as e:

        print(
            f"CSV 로딩 오류: {e}"
        )

        return pd.DataFrame()