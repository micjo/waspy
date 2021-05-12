from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for, make_response, send_from_directory, redirect
from flask_cors import CORS
import requests
import logging
import json
import plotly.graph_objects as go

lab_urls = {
    "motrona_rbs": "http://127.0.0.1:23000/api/latest",
    "aml_x_y": "http://127.0.0.1:22000/api/latest",
    "aml_det_theta": "http://127.0.0.1:22001/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22002/api/latest",
    "caen_charles_evans": "http://169.254.13.109:22123/api/latest",
}

home_urls = {
    "motrona_rbs": "http://127.0.0.1:22200/api/latest",
    "aml_x_y": "http://127.0.0.1:22100/api/latest",
    "aml_det_theta": "http://127.0.0.1:22100/api/latest",
    "aml_phi_zeta": "http://127.0.0.1:22100/api/latest",
    "caen_charles_evans": "http://olympus:22000/api/latest",
}

direct_urls = home_urls

hardware_config = {
        "aml_x_y" : {"type":"aml", "title": "AML X Y", "first_name":"X", "second_name":"Y", "first_load":"72.50", "second_load":"61.7"},
        "aml_phi_zeta" : {"type":"aml", "title": "AML Phi Zeta", "first_name":"Phi", "second_name":"Zeta", "first_load":"0.00", "second_load":"-1.00"},
        "aml_det_theta" : {"type":"aml", "title": "AML Det Theta", "first_name":"Detector", "second_name":"Theta", "first_load":"170.00", "second_load":"-180.50"},
        "motrona_rbs" : {"type":"motrona", "title" : "Motrona RBS"},
        "caen_charles_evans" : {"type":"caen", "title":"CAEN Charles Evans" }
}

from app.rbs_experiment.blueprints import make_blueprints as make_rbs_experiment_blueprints
rbs_blueprints = make_rbs_experiment_blueprints(direct_urls, hardware_config)

from app.hardware_controllers.blueprints import make_blueprints as make_hw_blueprints
hw_blueprints = make_hw_blueprints(direct_urls, hardware_config)

app = Flask(__name__)
app.register_blueprint(rbs_blueprints)
app.register_blueprint(hw_blueprints)

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").setLevel(logging.CRITICAL)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", config = hardware_config)



@app.route("/favicon.ico")
def favicon():
    return send_from_directory('static','favicon.png')
