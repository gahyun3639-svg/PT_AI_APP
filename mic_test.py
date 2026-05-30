import speech_recognition as sr

print("테스트 시작")

try:

    mic_list = sr.Microphone.list_microphone_names()

    print("마이크 개수:", len(mic_list))

    for index, name in enumerate(mic_list):

        print(index, ":", name)

except Exception as e:

    print("오류 발생:", e)

input("엔터 누르면 종료")