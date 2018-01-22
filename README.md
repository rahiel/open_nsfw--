# open_nsfw--

This is a fork of Yahoo's [open_nsfw][]. The goal is to make the *Not Suitable
for Work* (NSFW) classification model easily accessible through an HTTP API
deployable with Docker.

# Install

First [install Docker][docker] (available in Debian as [docker.io][dpkg]), then
give the user you want to run the API as permission to use Docker:
``` shell
sudo gpasswd -a $USER docker
```
You need to logout and login again for this to take effect.

Now build the image, this might take a while:
``` shell
docker build -t open_nsfw https://raw.githubusercontent.com/rahiel/open_nsfw--/master/Dockerfile
```

Then you can start the API:
``` shell
docker run -p <port>:8080 open_nsfw
```
where you replace `<port>` with the port number you want to have the API
accessible on your local machine.

[open_nsfw]: https://github.com/yahoo/open_nsfw
[docker]: https://docs.docker.com/engine/installation/
[dpkg]: https://packages.debian.org/sid/docker.io

# Usage

The API is very simple, you POST an `url` of an image and the API will then
fetch it, classify it and return the probability that it's NSFW. The probability
is expressed as a real number between 0 and 1.

In the following examples I assume you picked 8080 for the port number, so the
API is running at `localhost:8080`.

With curl:
``` shell
curl -d 'url=http://example.com/image.jpg' localhost:8080
```

With Python:
``` python
import requests
r = requests.post("http://localhost:8080", data={"url": "http://example.com/image.jpg"})
nsfw_prob = float(r.text)
```

# HTTP Errors

## 400 Bad Request: Missing `url` POST parameter

You need to specify `url` as a POST parameter.

## 404 Not Found

The requested `url` leads to an HTTP 404 Not Found error.

## 415 Unsupported Media Type: Invalid image

The requested `url` is not a valid image.
