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

RUN git clone https://github.com/cooperdk/open_nsfw_2022.git /opt/open_nsfw_2022 \
 && git checkout 7f7f24e0937f3df50704e4ad75eeb044688353f3

RUN pip3 install -r requirements.txt

EXPOSE 8080

RUN groupadd -r open_nsfw && useradd --no-log-init -r -g open_nsfw open_nsfw

USER open_nsfw

ENTRYPOINT ["python3", "api.py"]
