FROM ubuntu:20.04

WORKDIR /default-downloader

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "run.py"]