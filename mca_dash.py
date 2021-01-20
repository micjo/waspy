from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for, make_response, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route('/caen_max')
def caen_max():
    return render_template("caen_max.html")

@app.route("/aml_x_y")
def aml_x_y():
    return render_template("aml_max.html", prefix="aml_x_y", url='http://localhost:22000');

@app.route("/aml_det_theta")
def aml_det_theta():
    return render_template("aml_max.html", prefix="aml_det_theta", url='http://localhost:22001');

@app.route("/aml_phi_zeta")
def aml_phi_zeta():
    return render_template("aml_max.html", prefix="aml_phi_zeta", url='http://localhost:22002');

@app.route("/favicon.ico")
def favicon():
    return send_from_directory('static','favicon.png')

@app.route("/min_itf")
def min_itf():
    return render_template("min_itf.html");
