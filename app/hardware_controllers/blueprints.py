from flask import Blueprint, render_template, abort, jsonify, request
import requests, json

def get_page_type(hardwareType):
    if (hardwareType == "aml"): return "max_aml.html"
    if (hardwareType == "caen"): return "max_caen.html"
    if (hardwareType == "motrona"): return "max_motrona.html"

def make_blueprints(direct_url_config, hardware_config):
    hw_blueprints = Blueprint('hardware_controllers', __name__)

    @hw_blueprints.route("/api/<hw>/caps")
    def api_caps(hw):
        resp = requests.get(direct_url_config[hw] + "/caps")
        return resp.json(), resp.status_code

    @hw_blueprints.route("/api/<hw>/histogram/<board>-<channel>")
    def histogram(hw,board,channel):
        try:
            resp = requests.get(direct_url_config[hw]+"/histogram/"+board+"-"+channel)
            return resp.text, resp.status_code
        except:
            return jsonify(""), 404

    @hw_blueprints.route("/api/<hw>", methods=["POST", "GET"])
    def api_hw(hw):
        if request.method == "POST":
            data_string = request.data.decode('utf-8')
            json_request = json.loads(data_string)
            try:
                resp = requests.post(direct_url_config[hw], json=json_request)
                return jsonify(""), resp.status_code
            except:
                return jsonify(""), 404
        else:
            try:
                resp = requests.get(direct_url_config[hw])
                return resp.json(), resp.status_code
            except:
                return jsonify(""), 404

    @hw_blueprints.route("/hw/<hwType>")
    def hw(hwType):
        hardware = hardware_config[hwType]
        page_type = get_page_type(hardware["type"])
        return render_template(str(page_type), prefix = hwType, config = hardware)

    return hw_blueprints
