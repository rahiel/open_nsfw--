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
 && git checkout 3f439d0b85dc92cb2c05f80337f7537daaa3009c

RUN pip3 install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3", "api.py"]
