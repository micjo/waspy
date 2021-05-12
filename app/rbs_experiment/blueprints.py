from flask import Blueprint, render_template, abort, jsonify, request
import json, time, os, threading, errno
from app.rbs_experiment.experiment_runner import RbsRunner
from pathlib import Path

def read_json_from_file(file_path):
    with open(file_path) as watch_file:
        content = watch_file.read()
        try:
            json_exp = json.loads(content)
            return json_exp
        except Exception as err:
            print(err)


def check_folder(rbs_runner, path):
    Path.mkdir(Path(path) / "ongoing", exist_ok=True)
    Path.mkdir(Path(path) / "done", exist_ok=True)
    Path.mkdir(Path(path) / "failed", exist_ok=True)
    while True:
        scan_path = Path(path)
        files = [path for path in scan_path.iterdir() if path.is_file()]
        for f in files:
            experiment = read_json_from_file(f)
            if (experiment):
                f = f.rename(scan_path / "ongoing" / f.name)
                rbs_runner.run(experiment)
                f = f.rename(scan_path / "done" / f.name)
            else:
                f = f.rename(scan_path / "failed" / f.name)

        time.sleep(1)


def make_blueprints(direct_url_config, config):
    rbs_blueprints = Blueprint('rbs_experiment', __name__)
    rbs_runner = RbsRunner(direct_url_config)
    task = threading.Thread(target=check_folder, args=(rbs_runner,"/tmp/watch/"))
    task.start()

    @rbs_blueprints.route("/rbs")
    def rbs():
        return render_template("rbs.html")

    @rbs_blueprints.route("/rbs_hw")
    def rbs_hw():
        return render_template("rbs_hw.html", config = config)

    @rbs_blueprints.route("/api/exp/rbs", methods=["POST","GET"])
    def exp_rbs():
        if request.method == "POST":
            data_string = request.data.decode('utf-8')
            json_request = json.loads(data_string)
            rbs_runner.run_in_background(json_request)
            return jsonify("OK")
        else:
            return jsonify(rbs_runner.get_status())

    return rbs_blueprints

