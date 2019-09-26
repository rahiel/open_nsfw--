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
    python3-wheel \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/open_nsfw--

RUN git clone https://github.com/rahiel/open_nsfw--.git /opt/open_nsfw-- \
 && git checkout c55805c968cacad86c62a72c08edc1cb4edb61c8 

RUN pip3 install -r requirements.txt

EXPOSE 8080

RUN groupadd -r open_nsfw && useradd --no-log-init -r -g open_nsfw open_nsfw

USER open_nsfw

ENTRYPOINT ["python3", "api.py"]
