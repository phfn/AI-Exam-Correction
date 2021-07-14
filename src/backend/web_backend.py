import json
from preprocessing_interface import autodetect_expected_answers, autocorrect_exams

from flask import Flask, request
from PIL import Image

from Exam_container import Exam_container
from base64converter import convert_base64_pdf_to_base_64_img

app = Flask(__name__)


@app.route('/analyze_correct_exam/', methods=["POST"])
def analyze_correct_exams():
    """
    Backend for image selection from the correct exam.
    Return a exam_container that holds the infos.
    """
    exam_container = Exam_container.from_json(json.dumps(request.json))
    exam_container = autodetect_expected_answers(exam_container)
    return exam_container.to_json()


@app.route('/analyze_student_exams/', methods=["POST"])
def analyze_student_exams():
    """
    Backend for the student exams. 
    Return a exam_container that holds the infos.
    """
    exam_container = Exam_container.from_json(json.dumps(request.json))
    exam_container = autocorrect_exams(exam_container)
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
