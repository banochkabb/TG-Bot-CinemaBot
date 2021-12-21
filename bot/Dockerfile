FROM python:3.9-slim

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

VOLUME ['/app']
WORKDIR /app

ARG TG_TOKEN
ARG KINO_TOKEN
ENV TG_TOKEN=$TG_TOKEN
ENV KINO_TOKEN=$KINO_TOKEN

COPY . WORKDIR
CMD ["python3.9", "main.py"]
