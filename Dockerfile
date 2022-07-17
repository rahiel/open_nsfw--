FROM debian:buster-slim

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
    libffi-dev \
    libssl-dev \
    openssl && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/open_nsfw_2022

RUN git clone https://github.com/cooperdk/open_nsfw_2022.git /opt/open_nsfw_2022 \
 && git checkout 92b1331931db96f186b32571786f6732353b624f

RUN pip3 install -r requirements.txt

EXPOSE 8080

RUN groupadd -r open_nsfw && useradd --no-log-init -r -g open_nsfw open_nsfw

USER open_nsfw

ENTRYPOINT ["python3", "api.py"]
