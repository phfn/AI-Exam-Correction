from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=["POST"])
def api():
    print(f"Got request {request.json}")
    return json.dumps(request.json)

if __name__ == "__main__":
    print("Starte Web-Backend")
    app.run()
        
