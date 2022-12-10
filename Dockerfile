# syntax=docker/dockerfile:1

FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=__http/app.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

EXPOSE 80

CMD [ "python3", "-m" , "flask", "run" ]