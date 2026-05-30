import whisper
import re
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np


# ==========================
# 모델 로드
# ==========================
model = whisper.load_model(
    "base"
)


# ==========================
# 의학용어 보정
# ==========================
def fix_medical_terms(
    text
):

    correction_map = {

        "에이씨엘":
        "ACL",

        "알오엠":
        "ROM",

        "엠엠티":
        "MMT",

        "지엠에프엠":
        "GMFM",

        "오십견":
        "Frozen shoulder",

        "극상근":
        "Supraspinatus",

        "극하근":
        "Infraspinatus",

        "라크만":
        "Lachman test",

        "맥머레이":
        "McMurray test"
    }

    for k, v in (
        correction_map.items()
    ):

        text = text.replace(
            k,
            v
        )

    return text


# ==========================
# 노이즈 제거
# ==========================
def clean_audio(
    audio_path
):

    y, sr = librosa.load(
        audio_path,
        sr=None
    )

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
                text
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