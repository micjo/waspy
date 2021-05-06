import threading
import requests as rq
import time
from datetime import datetime

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
    def __init__(self, config):
        self._config = config
        self._samples = [ ["", None] ]*120
        self._positions = [ ["", None] ]*120
        self.aggregate_lock = threading.Lock()

    def aggregate(self):
        while True:
            response = rq.get("http://localhost:5000/api/"+self._config['motrona'][0]['id'])
            time.sleep(1)
            if response.status_code == 404:
                continue
            current = response.json()["current(nA)"]
            with self.aggregate_lock:
                timestampStr = datetime.now().strftime("%H:%M:%S")
                self._samples.append([timestampStr, current])
                del self._samples[0]

            response = rq.get("http://localhost:5000/api/"+self._config['aml'][0]['id'])
            motor_one_position = response.json()['motor_1_position']
            with self.aggregate_lock:
                timestampStr = datetime.now().strftime("%H:%M:%S")
                self._positions.append([timestampStr, motor_one_position])
                del self._positions[0]
                time.sleep(1)

    def getPositions(self):
        with self.aggregate_lock:
            return self._positions

    def getSamples(self):
        with self.aggregate_lock:
            return self._samples

    def run_in_background(self):
        back = threading.Thread(target=self.aggregate, args=())
        back.start()


if __name__ == "__main__":
    agg = Aggregator(rbs_config)
    agg.run_in_background()


    while True:
        print("im in the main")
        print(agg.getSamples())
        time.sleep(1)
