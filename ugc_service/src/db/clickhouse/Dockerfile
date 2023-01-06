FROM python:3.10

WORKDIR /clickhouse

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt update -y  \
    && pip install --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "migrator.py"]