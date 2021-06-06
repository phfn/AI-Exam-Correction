import io
import json
from io import BytesIO
import re
from pdf2image import convert_from_bytes
from base64 import b64decode, b64encode

from flask import Flask, request
from PIL import Image

from Document import Document
from Task import Task

app = Flask(__name__)


def base_64_to_PIL_Image(img_64: str) -> Image:
    """
    Converts a image represented as a base64 string to a PIL Image Object.
    """

    # data begins after ,
    img_bytes = b64decode(img_64.split(",")[1])
    img_buf = io.BytesIO(img_bytes)
    img_pil = Image.open(img_buf)

    return img_pil


def get_base64_datatype(s: str):
    """
    Determents the datatype of a base64 string.
    Works only with application/pdf and image
    """
    # data:image/png;base64
    # data:application/pdf;base64
    re_pdf = re.compile(r"^data:application\/pdf")
    re_img = re.compile(r"^data:image\/")
    if re_pdf.match(s):
        return "pdf"
    if re_img.match(s):
        return "img"
    raise ValueError("The string is not a pdf nor an image")


def convert_exams_to_PIL(exams: list[str]):
    """
    Convers a list of base64 images or pdfs into PIL Image objects
    """
    exames_pil = []
    for exame in exams:
        if get_base64_datatype(exame) == "pdf":
            exame = convert_pdf_to_img(exame)

        exames_pil.append(base_64_to_PIL_Image(exame))
    return exames_pil


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
        exams: A List of base64 encoded exams.
            Datatype can be image or application/pdf.
    """
    print(f"Got request {request}")
    img = base_64_to_PIL_Image(request.json["img"])
    document = Document(img)
    exams = convert_exams_to_PIL(request.json["exams"])
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


def convert_pdf_to_img(pdf_64: str) -> str:
    """
    Converts a pdf to an image.
    The pdf needs to be base64 encoded.
    The returned image is also base64 encoded.
    """
    pdf_64 = pdf_64.split(",")[1]
    pdf_bytes = b64decode(pdf_64)
    images = convert_from_bytes(pdf_bytes)

    image = concat_images(images)

    # convert PIL Image in b64 image
    im_file = BytesIO()
    image.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = b64encode(im_bytes)
    return "data:image/png;base64," + im_b64.decode()


@app.route('/pdf2img/', methods=["POST"])
def pdf2img():
    """ Backend for pdf conversion.  """
    # convert base64 pdf in PIL Image
    pdf_64 = request.json["pdf"]
    img_64 = convert_pdf_to_img(pdf_64)
    return json.dumps({"img": f"{img_64}"})


if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
