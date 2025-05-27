FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

ENV DIR_PATH=/data

EXPOSE 5000

CMD ["python", "-u", "run.py"]
