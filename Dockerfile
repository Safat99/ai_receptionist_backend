FROM python:slim-buster

RUN useradd safat

WORKDIR /home/safat

COPY requirements.txt .
RUN python -m venv venv

RUN yes| apt-get update \ 
    && yes |apt-get install python3-dev default-libmysqlclient-dev build-essential

RUN python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY src src
COPY migrations migrations
COPY manage.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP manage.py

RUN chown -R safat:safat ./
USER safat

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]

#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

