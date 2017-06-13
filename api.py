import asyncio

import aiohttp
import async_timeout
import numpy as np
import uvloop
from aiohttp import web

from classify_nsfw import caffe_preprocess_and_compute, load_model


nsfw_net, caffe_transformer = load_model()


def classify(image: bytes) -> np.float64:
    scores = caffe_preprocess_and_compute(image, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=["prob"])
    return scores[1]

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.read()

class API(web.View):
    async def post(self):
        request = self.request
        data = await request.post()
        try:
            image = await fetch(session, data["url"])
            nsfw_prob = classify(image)
            text = nsfw_prob.astype(str)
            return web.Response(text=text)
        except:
            raise web.HTTPBadRequest()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
session = aiohttp.ClientSession()
app = web.Application()
app.router.add_route("*", "/api", API)
web.run_app(app)
