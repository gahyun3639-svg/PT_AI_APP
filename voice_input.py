import speech_recognition as sr

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("듣는 중...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(
            audio,
            language="ko-KR"
        )

        print("인식:", text)

        return text

    except:
        return ""