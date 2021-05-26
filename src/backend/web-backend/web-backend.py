import io
import json
from base64 import b64decode

from flask import Flask, request
from PIL import Image

from interfaces.Document import Document
from interfaces.Task import Task

app = Flask(__name__)


def base_64_to_PIL_Image(img_64: str) -> Image:
    # data begins after ,
    img_bytes = b64decode(img_64.split(",")[1])
    img_buf = io.BytesIO(img_bytes)
    img_pil = Image.open(img_buf)

    return img_pil


@app.route('/', methods=["POST"])
def api():
    """
    Backend for image selection.
    Recives a information from the frontend as json
    The json should have the following contents:
        tasks: A List of tasks each containing:
            x: x position of the upper left corner
            y: y position of the upper left corner
            width: The width of the crop
            height: The height of the crop
        img: The image of the Document as a base64 string.
    """
    print(f"Got request {request}")
    img = base_64_to_PIL_Image(request.json["img"])
    document = Document(img)
    for task in request.json["tasks"]:
        document.tasks.append(Task(
            task["x"],
            task["y"],
            task["width"],
            task["height"],
            task["type"],
            "",
            100
            ))
    return json.dumps(request.json)


if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
