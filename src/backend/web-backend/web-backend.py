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


def concat_images(images):
    """
    Concat multiple PIL Images.
    They should have all are the same width and hight.
    """
    height = images[0].height
    width = images[0].width
    new_image = Image.new('RGB', (width, height * len(images)))

    for i, image in enumerate(images):
        new_image.paste(image, (0, i*height))

    return new_image


@app.route('/pdf2img/', methods=["POST"])
def pdf2img():
    """ Backend for pdf conversion.  """
    # convert base64 pdf in PIL Image
    pdf_64 = request.json["pdf"].split(",")[1]
    pdf_bytes = b64decode(pdf_64)
    images = convert_from_bytes(pdf_bytes)

    image = concat_images(images)

    # convert PIL Image in b64 image
    im_file = BytesIO()
    image.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = b64encode(im_bytes)

    return json.dumps({"img": f"data:image/png;base64,{im_b64.decode()}"})


if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
