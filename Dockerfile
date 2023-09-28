FROM python:3.11.5

ADD . /data

WORKDIR /data

RUN pip install -r requirements.txt

CMD ["python", "main.py"]