"""
Copyright 2016 Yahoo Inc.
Licensed under the terms of the 2 clause BSD license.
Please see LICENSE.txt in the project root for the terms.
"""

import argparse
import sys
from io import BytesIO

import caffe
import numpy as np
from PIL import Image


def resize_image(img_data, sz=(256, 256)):
    """
    Resize image. Please use this resize logic for best results, as it was used
    to generate the training dataset.
    :param bytes data:
        The image data
    :param sz tuple:
        The resized image dimensions
    :returns bytearray:
        A byte array with the resized image
    """
    im = Image.open(BytesIO(img_data))
    if im.mode != "RGB":
        im = im.convert("RGB")
    imr = im.resize(sz, resample=Image.BILINEAR)
    fh_im = BytesIO()
    imr.save(fh_im, format="JPEG")
    fh_im.seek(0)
    return bytearray(fh_im.read())

def caffe_preprocess_and_compute(pimg, caffe_transformer=None, caffe_net=None, output_layers=None):
    """
    Run a Caffe network on an input image after preprocessing it to prepare
    it for Caffe.
    :param PIL.Image pimg:
        PIL image to be input into Caffe.
    :param caffe.Net caffe_net:
        A Caffe network with which to process pimg after preprocessing.
    :param list output_layers:
        A list of the names of the layers from caffe_net whose outputs are to
        to be returned. If this is None, the default outputs for the network
        are returned.
    :return:
        Returns the requested outputs from the Caffe net.
    """
    if caffe_net is not None:

        # Grab the default output names if none were requested specifically.
        if output_layers is None:
            output_layers = caffe_net.outputs

        img_data_rs = resize_image(pimg, sz=(256, 256))
        image = caffe.io.load_image(BytesIO(img_data_rs))

        H, W, _ = image.shape
        _, _, h, w = caffe_net.blobs["data"].data.shape
        h_off = max((H - h) // 2, 0)
        w_off = max((W - w) // 2, 0)
        crop = image[h_off:h_off + h, w_off:w_off + w, :]
        transformed_image = caffe_transformer.preprocess("data", crop)
        transformed_image.shape = (1,) + transformed_image.shape

        input_name = caffe_net.inputs[0]
        all_outputs = caffe_net.forward_all(blobs=output_layers,
                                            **{input_name: transformed_image})

        outputs = all_outputs[output_layers[0]][0].astype(float)
        return outputs
    else:
        return []


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments: input file.
    parser.add_argument(
        "input_file",
        help="Path to the input image file"
    )

    # Optional arguments.
    parser.add_argument(
        "--model_def",
        help="Model definition file.",
        default="nsfw_model/deploy.prototxt"
    )
    parser.add_argument(
        "--pretrained_model",
        help="Trained model weights file.",
        default="nsfw_model/resnet_50_1by2_nsfw.caffemodel"
    )

    args = parser.parse_args()
    image_data = open(args.input_file, "rb").read()

    # Pre-load caffe model.
    nsfw_net = caffe.Net(args.model_def, args.pretrained_model, caffe.TEST)

    # Load transformer
    # Note that the parameters are hard-coded for best results
    caffe_transformer = caffe.io.Transformer({"data": nsfw_net.blobs["data"].data.shape})
    caffe_transformer.set_transpose("data", (2, 0, 1))             # move image channels to outermost
    caffe_transformer.set_mean("data", np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    caffe_transformer.set_raw_scale("data", 255)                   # rescale from [0, 1] to [0, 255]
    caffe_transformer.set_channel_swap("data", (2, 1, 0))          # swap channels from RGB to BGR

    # Classify.
    scores = caffe_preprocess_and_compute(image_data, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=["prob"])

    # Scores is the array containing SFW / NSFW image probabilities
    # scores[1] indicates the NSFW probability
    print("NSFW score: {}".format(scores[1]))


if __name__ == "__main__":
    main(sys.argv)
