FROM python:3.11-slim

WORKDIR /app

COPY src /app
COPY tests /tests

RUN pip install --no-cache-dir -r /app/requirements.txt -r /tests/requirements.txt

ENV DIR_PATH=/data

EXPOSE 5000

CMD ["python", "-u", "run.py"]
