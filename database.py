import pandas as pd
import streamlit as st


def load_database():

    try:

        df = pd.read_csv(
            "physio_db.csv",
            encoding="utf-8-sig"
        )

        df.fillna(
            "",
            inplace=True
        )

        return df

    except Exception as e:

        st.error(
            f"CSV 로딩 오류: {e}"
        )

        return pd.DataFrame()