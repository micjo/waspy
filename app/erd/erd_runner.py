import queue
from queue import Queue
from typing import List, Union

from app.erd.entities import ErdRqm, Erd, PositionCoordinates
from app.erd.erd_setup import ErdSetup, get_z_range
from hive_exception import HiveError
from threading import Thread, Lock
import time
import logging


def run_recipe(recipe: Erd, erd_setup: ErdSetup):
    erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
    erd_setup.wait_for_arrival()
    erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.spectrum_filename)
    erd_setup.start_acquisition()
    erd_setup.wait_for_acquisition_started()
    z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment)
    wait_time = recipe.measuring_time_sec/len(z_range)
    logging.info("positions: " + str(z_range) + "wait_time_sec between steps: " + str(wait_time) + ", total measurement time: " + str(recipe.measuring_time_sec))
    for z in z_range:
        erd_setup.move(z)
        time.sleep(recipe.measuring_time_sec/len(z_range))
    erd_setup.wait_for_acquisition_done()


class ErdRunner(Thread):
    rqms: Queue[ErdRqm]
    _erd_setup: ErdSetup
    error: Union[None, Exception]

    def __init__(self, erd_setup: ErdSetup):
        Thread.__init__(self)
        self._lock = Lock()
        self.rqms = Queue()
        self.error = None
        self._erd_setup = erd_setup

    def run_erd_rqm(self, erd_rqm: ErdRqm, erd_setup: ErdSetup):
        try:
            for recipe in erd_rqm.recipes:
                run_recipe(recipe, erd_setup)
        except HiveError as e:
            self.error = e

    def run(self):
        while True:
            rqm = self.rqms.get()
            print("retrieved rqm:" + str(rqm))
            t = Thread(target=self.run_erd_rqm, args=(rqm, self._erd_setup))
            t.start()
            #todo: some feedback here
            t.join()
