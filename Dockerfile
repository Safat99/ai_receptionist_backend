FROM python:3.8.10-slim-buster


WORKDIR /home/safat
RUN mkdir data\
    && cd data\
    && mkdir images face_data audios all_speaker_models\
    && cd ..


RUN yes| apt-get update \ 
    &&  apt-get -y install default-libmysqlclient-dev build-essential cmake ffmpeg libsm6 libxext6

COPY requirements.txt requirements.txt

# RUN venv/bin/pip install -U pip wheel cmake
RUN pip install -r requirements.txt
# RUN venv/bin/pip install gunicorn pymysql cryptography

# COPY src src
# COPY migrations migrations
# COPY manage.py boot.sh ./
# RUN chmod a+x /home/safat/boot.sh

ENV FLASK_APP manage.py 

# RUN chown -R safat:safat ./
# USER safat

# EXPOSE 5000
# ENTRYPOINT [ "./boot.sh" ]

#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

COPY . .
EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 --worker-class gevent manage:app
# CMD gunicorn -b 0.0.0.0:5000 --worker-class gevent --log-level debug manage:app
