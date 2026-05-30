from database import load_database
from keyword_matcher import find_keywords
from speech_to_text import transcribe_audio

db = load_database()

print("물리치료 AI 음성 학습 앱")
print("종료: exit")

while True:

    command = input(
        "\n엔터 누르면 듣기 시작 (종료: exit): "
    )

    if command.lower() == "exit":
        break

    print("⚠️ main.py는 현재 Streamlit 앱과 별개입니다.")
    print("🎙️ 음성 기능은 app.py에서 사용하세요.")

    query = input(
        "검색어 직접 입력: "
    )

    results = find_keywords(
        query,
        db
    )

    if not results:
        print("검색 결과 없음")
        continue

    for result in results:

        print("\n====================")

        print(
            f"용어: "
            f"{result.get('keyword', '')}"
        )

        print(
            f"신용어: "
            f"{result.get('new_term', '')}"
        )

        print(
            f"구용어: "
            f"{result.get('old_term', '')}"
        )

        print(
            f"영어: "
            f"{result.get('english', '')}"
        )

        print(
            f"평가: "
            f"{result.get('related_assessment', '')}"
        )

        print(
            f"운동: "
            f"{result.get('related_exercise', '')}"
        )

        print(
            f"주의: "
            f"{result.get('caution', '없음')}"
        )

        print("====================")