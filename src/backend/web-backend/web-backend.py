
# Adding paths of custom packages
import sys
sys.path.append('../../interfaces', '../preprocessing/')

from ocr-interface import check_document
from flask import Flask, request
import json
import Document



app = Flask(__name__)

@app.route('/', methods=["POST"])
def api():
    print(f"Got request {request.json}")
    return json.dumps(request.json)

if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
        
