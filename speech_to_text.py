import os
import whisper
import traceback
import re
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
from database import load_database

# ==========================
# 모델 로드
# ==========================
model = whisper.load_model(
    "base"
)
db = load_database()

# ==========================
# 의학용어 보정
# ==========================
def fix_medical_terms(
    text,
    db
):

    correction_map = {}

    # -------------------
    # CSV 전체 자동 읽기
    # -------------------
    for _, row in db.iterrows():

        standard_term = str(
            row.get(
                "keyword",
                ""
            )
        ).strip()

        if not standard_term:
            continue

        search_terms = []

        for col in [

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
            ).strip()

            if value:

                terms = [

                    x.strip()

                    for x in value.split(",")

                    if x.strip()
                ]

                search_terms.extend(
                    terms
                )

        for term in search_terms:

            correction_map[
                term.lower()
            ] = standard_term

    # -------------------
    # Whisper 오타 보정
    # -------------------
    def fix_medical_terms(
    text,
    db
):

        text_lower = (
        text.lower()
    )

    correction_map = {}

    for _, row in db.iterrows():

        # 기준 용어
        standard_term = str(
            row.get(
                "keyword",
                ""
            )
        ).strip()

        if not standard_term:
            continue

        # 검색 가능한 모든 컬럼
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
            ).strip()

            if not value:
                continue

            terms = [

                x.strip()

                for x in value
                .split(",")

                if x.strip()
            ]

            for term in terms:

                correction_map[
                    term.lower()
                ] = standard_term

    # -------------------
    # Whisper 오타 보정
    # -------------------
    typo_map = {

        "뇌졸증":
        "뇌졸중",

        "오십건":
        "오십견",

        "극상 군":
        "극상근",

        "극하 군":
        "극하근",

        "엠엔티":
        "MMT",

        "엠 엠 티":
        "MMT",

        "에이 엠 에스":
        "MAS",

        "알 오 엠":
        "ROM",

        "에이 씨 엘":
        "ACL",

        "피 씨 엘":
        "PCL",

        "맨손 근력 검사":
        "맨손근력검사",

        "근 긴장도 검사":
        "근긴장도검사",
    }

    for k, v in (
        typo_map.items()
    ):

        text = text.replace(
            k,
            v
        )

    text_lower = (
        text.lower()
    )

    matched_terms = []

    for k, v in (
        correction_map.items()
    ):

        if (
            k
            in
            text_lower
        ):

            matched_terms.append(
                v
            )

    # 중복 제거
    matched_terms = list(
        dict.fromkeys(
            matched_terms
        )
    )

    if matched_terms:

        return " ".join(
            matched_terms
        )

    return text


# ==========================
# 노이즈 제거
# ==========================
def clean_audio(
    audio_path
):

    try:

        y, sr = librosa.load(
            audio_path,
            sr=16000,
            mono=True
        )

        reduced_noise = (
            nr.reduce_noise(
                y=y,
                sr=sr
            )
        )

        # 무음 제거
        trimmed_audio, _ = (
            librosa.effects.trim(
                reduced_noise,
                top_db=45
            )
        )

        # 오디오가 너무 짧으면
        if len(trimmed_audio) < 1000:

            trimmed_audio = (
                reduced_noise
            )

        temp_path = (
            "clean_audio.wav"
        )

        sf.write(
            temp_path,
            trimmed_audio,
            sr
        )

        return temp_path

    except Exception:

        # 노이즈 제거 실패 시
        # 원본 사용
        return audio_path

    # 잡음 제거
    reduced_noise = (
        nr.reduce_noise(
            y=y,
            sr=sr
        )
    )

    # 무음 제거
    trimmed_audio, _ = (
        librosa.effects.trim(
            reduced_noise,
            top_db=25
        )
    )

    temp_path = (
        "clean_audio.wav"
    )

    sf.write(
        temp_path,
        trimmed_audio,
        sr
    )

    return temp_path


# ==========================
# STT
# ==========================
def transcribe_audio(
    audio_path
):

    try:

        cleaned_path = (
            clean_audio(
                audio_path
            )
        )
        # 빈 파일 방지
        audio_size = os.path.getsize(
            cleaned_path
        )

        if audio_size < 1000:

            return (
                "음성이 너무 짧거나 "
                "인식되지 않았습니다."
            )

        result = (
            model.transcribe(
                cleaned_path,
                language="ko"
            )
        )

        text = (
            result["text"]
            .strip()
        )

        text = (
        fix_medical_terms(
            text,
            db
        )
    )

        return text

    except Exception as e:

        import traceback

        error_detail = traceback.format_exc()

        return (
            f"오류: {str(e)}\n\n"
            f"{error_detail}"
        )