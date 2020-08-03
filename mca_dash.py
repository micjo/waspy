from flask import Flask, render_template, abort, request, jsonify, app, redirect, url_for


app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html",
        array=(0,1,2,5,6,8))

@app.route("/flask_example/<int:index>")
def flask_example(index):
    return render_template("flask_example.html", index=index)

@app.route('/post_example', methods=["GET", "POST"])
def post_example():
    if request.method == "POST":
        return redirect((url_for('welcome')))
    else:
        return render_template("post_example.html")
    