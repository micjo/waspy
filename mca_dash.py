from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html",
        array=(0,1,2,5,6,8))

@app.route("/det01_theta/<int:index>")
def det01_theta(index):
    return render_template("det01_theta.html", index=index)

@app.route('/phi_zeta', methods=["GET", "POST"])
def phi_zeta():
    if request.method == "POST":
        return redirect((url_for('welcome')))
    else:
        return render_template("phi_zeta.html")


@app.route("/aml_x_y", methods=["GET", "POST"])
def aml_x_y():
    if request.method == "POST":
        return redirect((url_for('aml_x_y')))
    else:
        return render_template("aml_x_y.html")


@app.route("/caen", methods=["GET", "POST"])
def caen():
    if request.method == "POST":
        return redirect((url_for('caen')))
    else:
        return render_template("caen.html")
    
@app.route("/min_itf", methods=["GET", "POST"])
def min_itf():
    if request.method == "POST":
        return redirect((url_for('min_itf')))
    else:
        return render_template("min_itf.html")

@app.route("/dashboard_v2", methods=["GET", "POST"])
def dashboard_v2():
    if request.method == "POST":
        return redirect((url_for('dashboard_v2')))
    else:
        return render_template("dashboard_v2.html")

labels = [
    '0', '1', '2', '3',
    '4', '5', '6', '7',
    '8', '9', '10', '11'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    1000.91, 1200.28, 1100.83, 1135.87,
    1140.29, 1122.30, 900, 800
]

labels2 = [
    '0', '1', '2', '3',
    '4', '5', '6', '7',
    '8', '9', '10', '11'
]

values2 = [
    967.67, 1190.89, 1079.75, 1349.19,
    1000.91, 1200.28, 1100.83, 1135.87,
    1140.29, 1122.30, 900, 800
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Beam Current', max=2000, 
        labels=line_labels, values=line_values,
        title2="Something else", labels2 = labels2, values2 = values2)
