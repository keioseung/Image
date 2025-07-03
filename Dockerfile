# 1. Python 3.10을 기반으로 한 슬림 이미지 사용
FROM python:3.10-slim

# 2. 시스템 패키지 업데이트 및 Tesseract OCR 설치
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 생성 및 이동
WORKDIR /app

# 4. 현재 디렉토리의 모든 파일을 컨테이너에 복사
COPY . /app

# 5. pip 업그레이드 및 requirements 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Streamlit 기본 포트 열기 (Railway의 기본 포트는 8080)
EXPOSE 8080

# 7. Streamlit 앱 실행 명령어
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
