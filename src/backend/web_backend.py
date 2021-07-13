import json
from preprocessing_interface import autodetect_expected_answers, autocorrect_exams

from flask import Flask, request
from PIL import Image

from Exam_container import Exam_container
from base64converter import convert_base64_pdf_to_base_64_img

app = Flask(__name__)


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
    exam_container = Exam_container.from_json(json.dumps(request.json))
    exam_container = autodetect_expected_answers(exam_container)
    exam_container = autocorrect_exams(exam_container)
    print(exam_container.correct_exam.tasks[0].expected_answer)
    return exam_container.to_json()


@app.route('/pdf2img/', methods=["POST"])
def pdf2img():
    """ Backend for pdf conversion.  """
    # convert base64 pdf in PIL Image
    pdf_64 = request.json["pdf"]
    img_64 = convert_base64_pdf_to_base_64_img(pdf_64)
    return json.dumps({"img": f"{img_64}"})


if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
