from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for, make_response, send_from_directory, redirect
from flask_cors import CORS
import requests
import json

app = Flask(__name__)

# contains all daemons
config = {
        "motrona_rbs": "http://127.0.0.1:23000/api/latest",
        "aml_x_y": "http://127.0.0.1:22000/api/latest",
        "aml_det_theta": "http://127.0.0.1:22001/api/latest",
        "aml_phi_zeta": "http://127.0.0.1:22002/api/latest",
        "caen_charles_evans": "http://olympus:22000/api/latest",
}

aml_config = [
    {"id":"aml_x_y", "title": "AML X Y", "first_name":"X", "second_name":"Y",
        "first_load":"72.50", "second_load":"61.7"},
    {"id":"aml_phi_zeta", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta",
        "first_load":"0.00", "second_load":"-1.00"},
    {"id":"aml_det_theta", "title": "AML Detector Theta", "first_name":"Detector", "second_name":"Theta",
        "first_load":"170.00", "second_load":"-180.50"}
]

caen_config = [
        {"id":"caen_charles_evans", "title":"CAEN Charles Evans" }
]

#motrona's should be seperate dictionary and rbs should only be 1 dictionary

rbs_aml_config = [
    {"id":"aml_x_y", "title": "AML X Y", "first_name":"X", "second_name":"Y",
        "first_load":"72.50", "second_load":"61.7"},
    {"id":"aml_phi_zeta", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta",
        "first_load":"0.00", "second_load":"-1.00"},
    {"id":"aml_det_theta", "title": "AML Detector Theta", "first_name":"Detector", "second_name":"Theta",
        "first_load":"170.00", "second_load":"-180.50"}
]

rbs_motrona_config = [
        {"id":"motrona_rbs", "title" : "Motrona RBS"}
]


@app.route("/api/caps/<hw>")
def api_caps(hw):
    resp = requests.get(config[hw] + "/caps")
    return resp.json(), resp.status_code

@app.route("/api/<hw>", methods=["POST", "GET"])
def api_hw(hw):
    if request.method == "POST":
        data_string = request.data.decode('utf-8')
        json_request = json.loads(data_string)
        try:
            resp = requests.post(config[hw], json=json_request)
            return jsonify(resp.text), resp.status_code
        except:
            return jsonify(""), 404
    else:
        try:
            resp = requests.get(config[hw])
            return resp.json(), resp.status_code
        except:
            return jsonify(""), 404

@app.route("/")
def dashboard():
    print("hello world")
    return render_template("dashboard.html")

@app.route("/rbs")
def rbs():
    return render_template("rbs.html")

@app.route("/rbs_hw")
def rbs_hw():
    return render_template("rbs_hw.html", aml_config = rbs_aml_config, motrona_config = rbs_motrona_config )

@app.route("/motrona_rbs")
def motrona_rbs():
    return render_template("max_motrona.html", prefix="motrona", title="Motrona", url="/api/motrona_rbs")

@app.route("/aml/<hwType>")
def aml(hwType):
    for element in aml_config:
        if element["id"] == hwType:
            return render_template("max_aml.html", config = element)
    abort(404)

@app.route('/caen')
def caen():
    return render_template("max_caen.html", config = caen_config[0])

@app.route("/favicon.ico")
def favicon():
    return send_from_directory('static','favicon.png')
