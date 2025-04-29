import base64
from flask import Flask, send_file
import h5py
from importlib import resources
from io import BytesIO
from jinja2 import Template
from myosotis_researches.CcGAN.internal import *
import numpy as np
import pandas as pd
from PIL import Image


def Image_to_Base64(image: Image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"


def datasets_to_html(indexes, datasets_path, list_path, template_path, img_size):

    N = len(indexes)

    # Get template
    with open(template_path, "r") as f:
        template = Template(f.read())

    # Get data
    with h5py.File(datasets_path, "r") as f:
        images = f["images"][:]
        index_train = f["index_train"][:]
        index_valid = f["index_valid"][:]
        labels = f["labels"][:]
        types = f["types"][:]
    images = images[indexes]
    labels = labels[indexes]
    types = types[indexes]

    # Get list
    df = pd.read_csv(list_path)
    tool_wears = df.iloc[indexes]["tool_wear"]
    surfaces = df.iloc[indexes]["surface"]
    image_names = df.iloc[indexes]["image_name"]

    # Transform data to base64
    images = np.transpose(images, (0, 2, 3, 1))
    images = [Image.fromarray(image) for image in images]
    images_base64 = [Image_to_Base64(image) for image in images]

    # Render template
    items = []
    for i in range(N):
        items.append(
            {
                "image": images_base64[i],
                "image_name": image_names.iloc[i],
                "label": labels[i],
                "type": types[i],
                "index": indexes[i],
            }
        )

    return template.render(
        indexes=indexes,
        datasets_path=datasets_path,
        list_path=list_path,
        template_path=template_path,
        items=items,
        img_size=img_size,
    )


def visualize_datasets(
    indexes,
    datasets_path,
    list_path,
    template_path=resources.files("myosotis_researches").joinpath(
        "CcGAN", "visualize", "src", "template.html"
    ),
    host="127.0.0.1",
    port=8000,
    debug=True,
    img_size=64,
):
    # Local server
    app = Flask(__name__)

    @app.route("/")
    def index():
        return datasets_to_html(
            indexes, datasets_path, list_path, template_path, img_size
        )

    @app.route("/style.css")
    def style():
        return send_file(
            resources.files("myosotis_researches").joinpath(
                "CcGAN", "visualize", "src", "style.css"
            )
        )

    app.run(host=host, port=port, debug=debug)


__all__ = ["visualize_datasets"]
