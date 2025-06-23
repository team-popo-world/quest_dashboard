# 1. 베이스 이미지
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt 복사 후 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . .

# 5. uvicorn 실행
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]