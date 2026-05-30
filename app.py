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

        # -------------------
        # Waveform
        # -------------------
        # -------------------
        # recording state
        # -------------------
        if "recording" not in st.session_state:
            st.session_state.recording = False

        # 시작 버튼 누르면
        if audio is None:
            st.session_state.recording = True

        # 녹음 완료되면
        if audio:
            st.session_state.recording = False

            st.markdown(
                """
                <style>

                .wave-box{
                    width:100%;
                    height:180px;
                    background:#071018;
                    border-radius:22px;
                    overflow:hidden;
                    position:relative;
                    margin-top:15px;
                }

                .wave-svg{
                    width:200%;
                    height:180px;

                    position:absolute;
                    top:0;
                    left:0;

                    animation:
                    moveWave
                    5s linear infinite;
                }

                .wave-line{

                    fill:none;

                    stroke:#00F0FF;

                    stroke-width:3;

                    filter:
                    drop-shadow(
                        0 0 8px
                        #00F0FF
                    )
                    drop-shadow(
                        0 0 20px
                        #00F0FF
                    );
                }

                @keyframes moveWave{

                    from{
                        transform:
                        translateX(0);
                    }

                    to{
                        transform:
                        translateX(-50%);
                    }
                }

                </style>

                <div class="wave-box">

                <svg
                class="wave-svg"
                viewBox="0 0 1200 180">

                <path
                class="wave-line"

                d="
                M0 90

                Q30 20 60 90
                T120 90
                T180 90
                T240 90
                T300 90
                T360 90
                T420 90
                T480 90
                T540 90
                T600 90
                T660 90
                T720 90
                T780 90
                T840 90
                T900 90
                T960 90
                T1020 90
                T1080 90
                T1140 90
                T1200 90
                "

                </svg>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------
        # 녹음 완료
        # -------------------
        if audio:

            st.success(
                "✅ 녹음 완료"
            )

            duration = round(
                len(audio["bytes"])
                / 32000,
                1
            )

            st.write(
                f"⏱ "
                f"{duration:.1f}초"
            )

            # 재생
            st.audio(
                audio["bytes"],
                format="audio/wav"
            )

            # -------------------
            # temp wav 저장
            # -------------------
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
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

                text = (
                    transcribe_audio(
                        temp_audio_path
                    )
                )

            st.text_area(
                "📝 텍스트 변환 결과",
                value=text,
                height=150
            )
            # =========================
            # 의학용어 자동 검색
            # =========================
            results = find_keywords(
                text,
                db
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
                            ## 🩺
                            {result.get('keyword','')}
                            """
                        )

                        st.write(
                            "🌍 영어명:",
                            result.get(
                                "english",
                                ""
                            )
                        )

                        st.write(
                            "📖 설명:",
                            result.get(
                                "description",
                                ""
                            )
                        )

                        st.write(
                            "📋 평가도구:",
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

                        st.write(
                            "⚡ 관련 검사:",
                            result.get(
                                "related_special_test",
                                ""
                            )
                        )

                        # -------------------
                        # 관련 질환 펼치기
                        # -------------------
                        with st.expander(
                            "🧠 관련 질환 보기"
                        ):

                            st.write(
                                result.get(
                                    "related_disease",
                                    ""
                                )
                            )

                        # -------------------
                        # ROM
                        # -------------------
                        rom_exists = any([
                            result.get(
                                "shoulder_rom"
                            ),
                            result.get(
                                "elbow_rom"
                            ),
                            result.get(
                                "wrist_rom"
                            ),
                            result.get(
                                "hip_rom"
                            ),
                            result.get(
                                "knee_rom"
                            ),
                            result.get(
                                "ankle_rom"
                            )
                        ])

                        if rom_exists:

                            st.markdown(
                                "### 📐 ROM"
                            )

                            cols = st.columns(6)

                            rom_list = [

                                (
                                    "Shoulder",
                                    "shoulder_rom"
                                ),

                                (
                                    "Elbow",
                                    "elbow_rom"
                                ),

                                (
                                    "Wrist",
                                    "wrist_rom"
                                ),

                                (
                                    "Hip",
                                    "hip_rom"
                                ),

                                (
                                    "Knee",
                                    "knee_rom"
                                ),

                                (
                                    "Ankle",
                                    "ankle_rom"
                                )
                            ]

                            for i, (
                                label,
                                key
                            ) in enumerate(
                                rom_list
                            ):

                                with cols[i]:

                                    st.metric(
                                        label,
                                        result.get(
                                            key,
                                            "-"
                                        )
                                    )

            else:

                st.warning(
                    "관련 의학 용어를 찾지 못했습니다."
                )

            # -------------------
            # 자동 검색
            # -------------------
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
                            ## 🩺
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
                            "🌍 영어명:",
                            result.get(
                                "english",
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

                        # 관련 질환 펼치기
                        with st.expander(
                            "🧠 관련 질환 보기"
                        ):

                            st.write(
                                result.get(
                                    "related_disease",
                                    ""
                                )
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