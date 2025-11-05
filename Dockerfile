FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
 && pip install fastapi uvicorn transformers torch==2.1.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
