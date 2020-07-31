FROM python:3.6.9

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY requirements.txt /passnfly/

WORKDIR /passnfly

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
