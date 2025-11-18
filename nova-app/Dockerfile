FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Ensure DB exists on container start
RUN python -c "import db; db.init_db()"

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
