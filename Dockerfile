FROM debian:stretch-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    caffe-cpu \
    git \
    python3 \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-setuptools \
    openssl \
    libffi-dev \
    libssl-dev \
    python3-wheel \ 
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/open_nsfw_2022

RUN git clone https://github.com/rahiel/open_nsfw--.git /opt/open_nsfw-- \
 && git checkout c38951ce080fe0d41041fca721da9eab96119112 

RUN pip3 install -r requirements.txt

EXPOSE 8080

RUN groupadd -r open_nsfw && useradd --no-log-init -r -g open_nsfw open_nsfw

USER open_nsfw

ENTRYPOINT ["python3", "api.py"]
