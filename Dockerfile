FROM ubuntu:20.04

WORKDIR /default-downloader

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg

RUN python3 -m pip install --force-reinstall https://github.com/redraskal/yt-dlp/archive/refs/heads/fix/tiktok-user.zip

RUN playwright install && playwright install-deps

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "run.py"]