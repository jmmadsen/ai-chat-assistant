FROM python:3.11.6-slim-buster

COPY requirements.txt /

RUN pip3 install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip3 install -r /requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]