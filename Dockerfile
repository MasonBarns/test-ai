FROM python:3.10

WORKDIR /app

COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn transformers torch

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
