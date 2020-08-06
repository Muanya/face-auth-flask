FROM python:3.7-slim

RUN useradd face_auth

# set a directory for the app
WORKDIR /home/flask_app

COPY requirements.txt requirements.txt
RUN python -m venv venv

# install dependencies
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn 

COPY app app
COPY migrations migrations
COPY face_enc face_enc
COPY config.py manage.py boot.sh ./
RUN chmod +x boot.sh

ENV APP_SETTINGS "config.DevelopmentConfig"

RUN chown -R face_auth:face_auth ./
USER face_auth 

# define the port number the container should expose
EXPOSE 5000

# run the command
ENTRYPOINT ["./boot.sh"]
