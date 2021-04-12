from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for, make_response, send_from_directory, redirect
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)


config = {
        "motrona_rbs": "http://localhost:22000/api/latest"
}


@app.route("/")
def dashboard():
    print("hello world")
    return render_template("dashboard.html")

@app.route("/min_itf")
def min_itf():
    return render_template("min_itf.html")


@app.route("/motrona_rbs")
def ui_motrona_rbs():
    resp = requests.get(config["motrona_rbs"] + "/caps")
    return render_template("max_motrona.html", prefix ="motrona", url="/api/motrona_rbs")

@app.route("/api/motrona_rbs/caps")
def api_motrona_rbs_caps():
    resp = requests.get("http://localhost:22000/api/latest/caps")
    resp = requests.get(config["motrona_rbs"] + "/caps")
    return resp.json(), resp.status_code

@app.route("/api/motrona_rbs", methods=["POST", "GET"])
def api_motrona_rbs():
    if request.method == "POST":
        data_string = request.data.decode('utf-8')
        json_request = json.loads(data_string)
        resp = requests.post(config["motrona_rbs"], json=json_request)
        return jsonify(resp.text), resp.status_code
    else:
        resp = requests.get(config["motrona_rbs"])
        return resp.json(), resp.status_code


@app.route('/caen_max')
def caen_max():
    return render_template("caen_max.html")


@app.route("/aml_x_y")
def aml_x_y():
    return render_template("aml_max.html", prefix="aml_x_y", url='http://169.254.166.218:22000', 
    	load_first='72.50', load_second='61.7', first_name='X', second_name='Y');

@app.route("/aml_det_theta")
def aml_det_theta():
    return render_template("aml_max.html", prefix="aml_det_theta", url='http://169.254.166.218:22001', 
    	load_first='170.00', load_second='-180.50', first_name='Det', second_name='Theta');

@app.route("/aml_phi_zeta")
def aml_phi_zeta():
    return render_template("aml_max.html", prefix="aml_phi_zeta", url='http://169.254.166.218:22002',
    	load_first='0.00', load_second='-1.00', first_name='Phi', second_name='Zeta');

@app.route("/favicon.ico")
def favicon():
    return send_from_directory('static','favicon.png')

