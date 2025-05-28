FROM python:3.11-slim

RUN adduser --disabled-password --gecos '' flaskuser

WORKDIR /src

COPY src /src
COPY tests /tests

RUN mkdir /tests/.pytest_cache && \
	chown -R flaskuser:flaskuser /tests
USER flaskuser

RUN pip install --no-cache-dir -r /src/requirements.txt -r /tests/requirements.txt

ENV DIR_PATH=/data

EXPOSE 5000

CMD ["python", "-u", "run.py"]
