import os

# 인코딩 문제 방지
os.environ["PYTHONIOENCODING"] = "utf-8"

from pyngrok import ngrok


# 기존 세션 정리
ngrok.kill()

# 공유 링크 생성
public_url = ngrok.connect(
    addr=8501,
    bind_tls=True
)

print("\n공유 링크:")
print(public_url.public_url)
