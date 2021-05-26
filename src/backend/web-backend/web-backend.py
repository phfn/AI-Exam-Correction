import json
from base64 import b64decode, b64encode
from io import BytesIO

from flask import Flask, request
from pdf2image import convert_from_bytes
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=["POST"])
def api():
    print(f"Got request {request.json}")
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
