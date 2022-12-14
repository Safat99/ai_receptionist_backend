FROM python:3.8.10-slim-buster
RUN python -m pip install --upgrade pip
RUN useradd safat


WORKDIR /home/safat

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN yes| apt-get update \ 
    &&  apt-get -y install python3-dev default-libmysqlclient-dev build-essential cmake ffmpeg libsm6 libxext6


RUN venv/bin/pip install -U pip wheel cmake
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY src src
COPY migrations migrations
COPY manage.py boot.sh ./
RUN chmod a+x /home/safat/boot.sh

ENV FLASK_APP manage.py 

RUN chown -R safat:safat ./
USER safat

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]

#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

