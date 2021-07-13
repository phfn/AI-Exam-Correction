import re
from io import BytesIO
from base64 import b64decode, b64encode

from pdf2image import convert_from_bytes
from PIL import Image


def base_64_to_PIL_Image(img_64: str) -> Image.Image:
    """
    Converts a image represented as a base64 string to a PIL Image Object.
    """

    # data begins after ,
    img_bytes = b64decode(img_64.split(",")[1])
    img_buf = BytesIO(img_bytes)
    img_pil = Image.open(img_buf)

    return img_pil


def PIL_Image_to_base_64(img_pil: Image.Image) -> str:
    """
    Converts a image represented as a PIL Image Object to a base64 represetation of the image.
    """
    buffer = BytesIO()
    img_pil.save(buffer, format="PNG")
    img_str = b64encode(buffer.getvalue()).decode()

    return "data:image/png;base64," + img_str


def get_base64_datatype(s: str):
    """
    Determents the datatype of a base64 string.
    Works only with application/pdf and image
    """
    # data:image/png;base64
    # data:application/pdf;base64
    re_pdf = re.compile(r"^data:application/pdf")
    re_img = re.compile(r"^data:image/")
    if re_pdf.match(s):
        return "pdf"
    if re_img.match(s):
        return "img"
    raise ValueError("The string is not a pdf nor an image")


def convert_base64_exams_to_PIL(exams: list[str]):
    """
    Convers a list of base64 images or pdfs into PIL Image objects
    """
    exames_pil = []
    for exam in exams:
        if get_base64_datatype(exam) == "pdf":
            exam = convert_base64_pdf_to_base_64_img(exam)

        exames_pil.append(base_64_to_PIL_Image(exam))
    return exames_pil


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


def convert_base64_pdf_to_base_64_img(pdf_64: str) -> str:
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
