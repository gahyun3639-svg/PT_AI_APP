import streamlit as st
import tempfile

from streamlit_mic_recorder import (
    mic_recorder
)

from database import load_database
from keyword_matcher import find_keywords
from speech_to_text import (
    transcribe_audio
)

# =====================================
# PAGE
# =====================================
st.set_page_config(
    page_title="PHYSIO",
    layout="wide"
)

st.title("PHYSIO")

st.caption(
    "AI Physical Therapy Assistant"
)

db = load_database()

# =====================================
# TAB
# =====================================
tab1, tab2, tab3 = st.tabs(
    [
        "녹음",
        "검색",
        "파일"
    ]
)


# =====================================
# 녹음 탭
# =====================================
with tab1:

    st.subheader(
        "음성 기록기"
    )

    with st.container(
        border=True
    ):

        # -------------------
        # 녹음 버튼
        # -------------------
        audio = mic_recorder(
            start_prompt=
            "🎙 녹음 시작",

            stop_prompt=
            "⏹ 녹음 종료",

            just_once=False,

            use_container_width=True,

            key="physio_mic"
        )

        st.info(
        "🎙 녹음 버튼을 눌러 음성을 입력하세요"
    )
        
        # -------------------
        # 녹음 완료
        # -------------------
        if audio:

        # -------------------
        # 이전 결과 초기화
        # -------------------
            st.session_state[
                "matched_terms"
            ] = []

            st.session_state[
                "transcript"
            ] = ""

            st.session_state[
                "matched_terms"
            ] = []

            st.session_state[
                "transcript"
            ] = ""

            st.success(
                "✅ 녹음 완료"
            )

            duration = round(
                len(audio["bytes"])
                / 32000,
                1
            )

            st.write(
                f"⏱ {duration:.1f}초"
            )

            st.audio(
                audio["bytes"],
                format="audio/wav"
            )
            # -------------------
            # temp wav 저장
            # -------------------
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".webm"
            ) as tmp_file:

                tmp_file.write(
                    audio["bytes"]
                )

                temp_audio_path = (
                    tmp_file.name
                )

            # -------------------
            # 텍스트 변환
            # -------------------
            with st.spinner(
            "텍스트 변환 중..."
        ):

                audio_path = (
                    temp_audio_path
                )

                transcript = (
                    transcribe_audio(
                        audio_path
                    )
                )

            st.session_state[
                "transcript"
            ] = transcript
                

            
            st.text_area(
                "📝 텍스트 변환 결과",
                value=transcript,
                height=150
            )

            # =========================
            # 의학용어 자동 검색
            # =========================
            results = find_keywords(
                transcript,
                db
            )

            if results:

                st.markdown(
                    "## 🩺 관련 의학 정보"
                )

                for result in results:

                    keyword = result.get(
                        "keyword",
                        "알 수 없음"
                    )

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"## 🩺 {keyword}"
                        )

                        english = result.get(
                            "english",
                            ""
                        )

                        if english:
                            st.write(
                                "🌍 영어명:",
                                english
                            )

                        col1, col2 = st.columns(2)

                        with col1:

                            old_term = result.get(
                                "old_term",
                                ""
                            )

                            if old_term:
                                st.write(
                                    "📚 구용어:",
                                    old_term
                                )

                        with col2:

                            new_term = result.get(
                                "new_term",
                                ""
                            )

                            if new_term:
                                st.write(
                                    "🆕 신용어:",
                                    new_term
                                )

                        description = result.get(
                            "description",
                            ""
                        )

                        if description:
                            st.write(
                                "📖 설명:",
                                description
                            )

                        clinical = result.get(
                            "clinical_feature",
                            ""
                        )

                        if clinical:
                            st.write(
                                "🧠 임상 특징:",
                                clinical
                            )

                        disease = result.get(
                            "related_disease",
                            ""
                        )

                        if disease:

                            with st.expander(
                                "🦠 관련 질환"
                            ):

                                st.write(
                                    disease
                                )

                        assessment = result.get(
                            "related_assessment",
                            ""
                        )

                        if assessment:
                            st.write(
                                "📋 평가도구:",
                                assessment
                            )

                        tool = result.get(
                            "tool_used",
                            ""
                        )

                        if tool:
                            st.write(
                                "🛠 평가 툴:",
                                tool
                            )

                        normal_rom = result.get(
                            "normal_rom",
                            ""
                        )

                        if normal_rom:

                            with st.expander(
                                "📐 정상 ROM"
                            ):

                                for rom in str(
                                    normal_rom
                                ).split("|"):

                                    st.markdown(
                                        f"- {rom}"
                                    )

                        mmt = result.get(
                            "mmt_grade",
                            ""
                        )

                        if mmt:

                            with st.expander(
                                "💪 MMT Grade"
                            ):

                                for grade in str(
                                    mmt
                                ).split("|"):

                                    st.markdown(
                                        f"- {grade}"
                                    )

                        special = result.get(
                            "related_special_test",
                            ""
                        )

                        if special:
                            st.write(
                                "🧪 관련 검사:",
                                special
                            )

                        exercise = result.get(
                            "related_exercise",
                            ""
                        )

                        if exercise:
                            st.write(
                                "🏋️ 운동:",
                                exercise
                            )

                        protocol = result.get(
                            "exercise_protocol",
                            ""
                        )

                        if protocol:

                            with st.expander(
                                "📋 운동 프로토콜"
                            ):

                                st.write(
                                    protocol
                                )

                        tip = result.get(
                            "clinical_tip",
                            ""
                        )

                        if tip:
                            st.info(
                                f"💡 {tip}"
                            )

            else:

                st.warning(
                    "관련 의학 용어를 찾지 못했습니다."
                )


# =====================================
# 검색 탭
# =====================================
with tab2:

    st.subheader("용어 검색")

    query = st.text_input(
        "검색어 입력",
        placeholder="예: ACL, 오십견, 극상근",
        key="search_input_unique"
    )

    if query:

        results = find_keywords(query, db)

        if results:

            st.markdown("## 🔍 검색 결과")

            for result in results:

                keyword = result.get(
                    "keyword",
                    "알 수 없음"
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"## 🩺 {keyword}"
                    )

                    st.write(
                        "🌍 영어명:",
                        result.get(
                            "english",
                            "-"
                        )
                    )

                    st.write(
                        "📖 설명:",
                        result.get(
                            "description",
                            "-"
                        )
                    )

                    st.write(
                        "🧠 임상 특징:",
                        result.get(
                            "clinical_feature",
                            "-"
                        )
                    )

                    if result.get(
                        "related_disease"
                    ):

                        with st.expander(
                            "🧠 관련 질환"
                        ):

                            st.write(
                                result.get(
                                    "related_disease"
                                )
                            )

                    if result.get(
                        "related_assessment"
                    ):

                        with st.expander(
                            "📋 평가도구"
                        ):

                            st.write(
                                result.get(
                                    "related_assessment"
                                )
                            )

                    if result.get(
                        "related_exercise"
                    ):

                        with st.expander(
                            "🏋️ 운동"
                        ):

                            st.write(
                                result.get(
                                    "related_exercise"
                                )
                            )

        else:

            st.warning(
                "검색 결과 없음"
            )

# =====================================
# 파일 탭
# =====================================
with tab3:

    st.subheader(
        "AI 파일 분석"
    )

    uploaded_file = (
        st.file_uploader(
            "CSV / 이미지 업로드",
            type=[
                "csv",
                "png",
                "jpg",
                "jpeg"
            ]
        )
    )

    if uploaded_file:

        file_type = (
            uploaded_file.type
        )

        # =====================
        # CSV
        # =====================
        if "csv" in file_type:

            import pandas as pd

            df = pd.read_csv(
                uploaded_file,
                encoding=
                "utf-8-sig"
            )

            st.success(
                "CSV 업로드 완료"
            )

            st.markdown(
                "## 📊 데이터 미리보기"
            )

            st.dataframe(
                df.head(10)
            )

            st.markdown(
                "## 🧠 AI 분석"
            )

            st.write(
                f"행 개수: "
                f"{len(df)}"
            )

            st.write(
                f"열 개수: "
                f"{len(df.columns)}"
            )

            st.write(
                "컬럼:"
            )

            st.write(
                list(df.columns)
            )

            # 키워드 분석
            text = " ".join(
                map(
                    str,
                    df.columns
                )
            )

            results = (
                find_keywords(
                    text,
                    db
                )
            )

            if results:

                st.markdown(
                    "## 🩺 관련 의학 정보"
                )

                for result in results:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"""
                            ### 🩺
                            {result.get('keyword','')}
                            """
                        )

                        st.write(
                            "📖 설명:",
                            result.get(
                                "description",
                                ""
                            )
                        )

                        st.write(
                            "📋 평가:",
                            result.get(
                                "evaluation_tool",
                                ""
                            )
                        )

                        st.write(
                            "🏋️ 운동:",
                            result.get(
                                "exercise_protocol",
                                ""
                            )
                        )

        # =====================
        # 이미지
        # =====================
        elif (
            "image"
            in file_type
        ):

            st.success(
                "이미지 업로드 완료"
            )

            st.image(
                uploaded_file,
                use_container_width=
                True
            )

            st.markdown(
                "## 🧠 이미지 기반 분석"
            )

            file_name = (
                uploaded_file.name
                .lower()
            )

            # 이름 기반 1차 추정
            results = (
                find_keywords(
                    file_name,
                    db
                )
            )

            if results:

                for result in results:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"""
                            ### 🩺
                            {result.get('keyword','')}
                            """
                        )

                        st.write(
                            "📖 설명:",
                            result.get(
                                "description",
                                ""
                            )
                        )

                        st.write(
                            "🧠 특징:",
                            result.get(
                                "clinical_feature",
                                ""
                            )
                        )

                        st.write(
                            "📋 평가:",
                            result.get(
                                "evaluation_tool",
                                ""
                            )
                        )

                        st.write(
                            "🏋️ 운동:",
                            result.get(
                                "exercise_protocol",
                                ""
                            )
                        )

            else:

                st.info(
                    "이미지 이름 기반 "
                    "관련 질환 없음"
                )