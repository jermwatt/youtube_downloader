# copied from base dockerfile provided by https://docs.streamlit.io/deploy/tutorials/docker
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

ENV PYTHONPATH=.

RUN git clone https://github.com/jermwatt/youtube_downloader .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/home/youtube_downloader/app.py", "--server.port=8501", "--server.address=0.0.0.0"]