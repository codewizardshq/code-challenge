import pyduktape
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/js/eval", methods=["POST"])
def js_eval():
    """Eval some JavaScript using pyduktape"""

    if not request.is_json:
        return jsonify(error="payload must be JSON format"), 400

    data = request.get_json()

    try:
        code = data["code"]
    except KeyError:
        return jsonify(error="missing 'code' parameter"), 400

    ctx = pyduktape.DuktapeContext()

    output = ""
    error = ""

    try:
        output = ctx.eval_js(code)
    except Exception as e:
        error = str(e)

    return jsonify(output=output, error=error)
