FROM python:3.12.4-slim

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y curl

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py app.py
COPY settings.example.cfg settings.cfg

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]