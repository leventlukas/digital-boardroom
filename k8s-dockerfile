FROM python:3

COPY ./code/requirements.txt .
RUN pip install -r requirements.txt

COPY /code/* ./usr/src/app/

WORKDIR /usr/src/app

EXPOSE 8404

CMD ["python", "server.py"]
