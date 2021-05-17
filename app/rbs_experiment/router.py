import json, time, os, threading, errno
from app.rbs_experiment.experiment_runner import RbsRunner
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
import asyncio
import app.rbs_experiment.rbs_experiment as rbs

templates = Jinja2Templates(directory="templates")



runner = rbs.RbsExperiment()
asyncio.create_task(runner.run_main())

def rbs_router(direct_url_config, config):
    router = APIRouter()

    @router.get("/rbs_hw", response_class=HTMLResponse, tags=["WebUI"])
    async def rbs_hw(request: Request):
        return templates.TemplateResponse("rbs_hw.html", {"request":request, "config": config})

    @router.get("/api/exp/rbs", tags=["RBS API"])
    async def get_rbs_experiment():
        return runner.status


    # @rbs_blueprints.route("/api/exp/rbs", methods=["POST","GET"])
    # def exp_rbs():
        # if request.method == "POST":
            # data_string = request.data.decode('utf-8')
            # json_request = json.loads(data_string)
            # rbs_runner.run_in_background(json_request)
            # return jsonify("OK")
        # else:
            # return jsonify(rbs_runner.get_status())

    return router
    # return rbs_blueprints

