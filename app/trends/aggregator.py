import asyncio
import threading
import requests as rq
from datetime import datetime
from app.config.config import DaemonConfig

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

motrona_config = [
    {"id":"motrona_rbs", "title" : "Motrona RBS"}

]

rbs_config = {
   "aml" : aml_config,
   "caen" : caen_config,
   "motrona" : motrona_config
}


class Aggregator:
    def __init__(self, config: DaemonConfig):
        self._config = config
        self._samples = [ ["inf", 0] ]*120
        self._positions = [ ["inf", 0] ]*120
        self.aggregate_lock = threading.Lock()

#should switch these to aiohttp
    def aggregate(self):
        timestampStr = datetime.now().strftime("%H:%M:%S")
        response = rq.get(self._config.motrona_rbs.url)
        if response.status_code == 404:
            return
        current = response.json()["current(nA)"]
        with self.aggregate_lock:
            self._samples.append([timestampStr, current])
            del self._samples[0]

        response = rq.get(self._config.aml_x_y.url)
        motor_one_position = response.json()['motor_1_position']
        with self.aggregate_lock:
            self._positions.append([timestampStr, motor_one_position])
            del self._positions[0]

    def getPositions(self):
        with self.aggregate_lock:
            return self._positions

    def getSamples(self):
        with self.aggregate_lock:
            return self._samples

    async def run_main(self):
        while True:
            await asyncio.sleep(1)
            self.aggregate()


# if __name__ == "__main__":
    # agg = Aggregator(rbs_config)
    # agg.run_in_background()


    # while True:
        # print("im in the main")
        # print(agg.getSamples())
        # time.sleep(1)
