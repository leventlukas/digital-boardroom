FROM python:3

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY /code/* ./usr/src/app/

WORKDIR /usr/src/app

CMD ["python", "server.py"]