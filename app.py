from quart import Quart, jsonify, request
from quart_cors import cors

from QR_codes import *

app = Quart(__name__)
app = cors(app)


@app.route("/report", methods=["GET"])
async def get_Menu():
    report = request.args.get("report_data")
    if report:
        base64_code = generate_qr_code_from_json(report)
        return jsonify({"report": base64_code})
    else:
        return jsonify({"error": "No report provided"}), 400


@app.route("/test", methods=["GET"])
async def get_test():

    return jsonify([{"name": "eman", "id": "1"}, {"name": "eman", "id": "2"},{"name": "eman", "id": "3"}])


@app.route("/barCodes", methods=["GET"])
async def get_barCode():

    id = request.args.get("barCodeid")
    return jsonify({"id": id, "status": 0})


if __name__ == "__main__":
    app.run(debug=True)
