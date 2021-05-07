from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for, make_response, send_from_directory, redirect
from flask_cors import CORS
import requests
import json
import rbs

import aggregator as agg

app = Flask(__name__)

# contains all daemons
config = {
    "motrona_rbs": "http://127.0.0.1:22200/api/latest",
    "aml_x_y": "http://127.0.0.1:22100/api/latest",
    "aml_det_theta": "http://127.0.0.1:22100/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22100/api/latest",
    "caen_charles_evans": "http://127.0.0.1:22300/api/latest",
}

root_config = {
        "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":"72.50", "second_load":"61.7"},
        "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":"0.00", "second_load":"-1.00"},
        "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":"170.00", "second_load":"-180.50"},
        "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS"},
        "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans" }
}

# aggregator = agg.Aggregator(rbs_config)
# aggregator.run_in_background()
rbs_runner = rbs.RbsRunner(config)

@app.route("/trends/rbs_current")
def rbs_current():
    return jsonify(aggregator.getSamples())

@app.route("/trends/aml_positions")
def aml_position():
    return jsonify(aggregator.getPositions())

@app.route("/api/<hw>/caps")
def api_caps(hw):
    resp = requests.get(config[hw] + "/caps")
    return resp.json(), resp.status_code

@app.route("/api/exp/rbs", methods=["POST","GET"])
def exp_rbs():
    if request.method == "POST":
        data_string = request.data.decode('utf-8')
        json_request = json.loads(data_string)
        rbs_runner.run_in_background(json_request)
        return jsonify("OK")
    else:
        return jsonify(rbs_runner.get_status())


@app.route("/api/<hw>/histogram/<board>-<channel>")
def histogram(hw,board,channel):
    try:
        resp = requests.get(config[hw]+"/histogram/"+board+"-"+channel)
        return resp.text, resp.status_code
    except:
        return jsonify(""), 404

@app.route("/api/<hw>", methods=["POST", "GET"])
def api_hw(hw):
    if request.method == "POST":
        data_string = request.data.decode('utf-8')
        json_request = json.loads(data_string)
        try:
            print("sending to " + config[hw])
            resp = requests.post(config[hw], json=json_request)
            return jsonify(""), resp.status_code
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
    return render_template("dashboard.html", config = root_config)

@app.route("/rbs")
def rbs():
    return render_template("rbs.html")

def get_page_type(hardwareType):
    if (hardwareType == "aml"): return "max_aml.html"
    if (hardwareType == "caen"): return "max_caen.html"
    if (hardwareType == "motrona"): return "max_motrona.html"

y_values=[0,1,2,3,4]
@app.route("/graph")
def graph():
    global y_values
    y_values = [x+1 for x in y_values]
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=y_values)
    return fig.to_html(include_plotlyjs=False)

@app.route("/rbs_hw")
def rbs_hw():
    return render_template("rbs_hw.html", config = root_config)

@app.route("/hw/<hwType>")
def hw(hwType):
    print(hwType)
    hardware = root_config[hwType]
    page_type = get_page_type(hardware["type"])
    return render_template(page_type, prefix = hwType, config = hardware)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory('static','favicon.png')
