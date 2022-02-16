import logging
import time
from collections import deque
from threading import Thread, Lock
from typing import List, Dict

from app.rqm.rqm_action_plan import RqmActionPlan, EmptyRqmActionPlan, empty_action_plan


class RqmRunner(Thread):
    _scheduled_rqms: List[RqmActionPlan]
    _past_rqms: deque[RqmActionPlan]
    _failed_rqms: deque[RqmActionPlan]
    _active_rqm: RqmActionPlan
    _abort: bool
    _lock: Lock
    _run_status: str

    def __init__(self):
        Thread.__init__(self)
        self._scheduled_rqms = []
        self._abort = False
        self._past_rqms = deque(maxlen=5)
        self._failed_rqms = deque(maxlen=5)
        self._active_rqm = EmptyRqmActionPlan()
        self._run_status = "Idle"
        self._lock = Lock()

    def abort_active(self) -> None:
        with self._lock:
            self._active_rqm.abort()

    def abort_schedule(self) -> None:
        with self._lock:
            self._scheduled_rqms = []

    def get_state(self) -> Dict:
        with self._lock:
            rqms = _serialize_rqm_list(self._scheduled_rqms)
            past_rqms = _serialize_rqm_list(list(self._past_rqms))
            failed_rqms = _serialize_rqm_list(list(self._failed_rqms))
            active_rqm = self._active_rqm.serialize()
        state = {"run_status": self._run_status, "schedule": rqms, "active_rqm": active_rqm, "done": past_rqms,
                 "failed": failed_rqms}
        return state

    def add_rqm_to_queue(self, rqm: RqmActionPlan):
        logging.info("adding rqm to queue")
        with self._lock:
            self._scheduled_rqms.append(rqm)

    def run(self):
        while True:
            time.sleep(1)
            rqm = self._pop_rqm()
            self._set_active_rqm(rqm)
            if not rqm.empty():
                rqm.execute()
                if rqm.completed():
                    self._past_rqms.appendleft(rqm)
                else:
                    self._failed_rqms.appendleft(rqm)

    def _set_active_rqm(self, rqm):
        with self._lock:
            self._active_rqm = rqm
            self._run_status = "Idle" if rqm.empty() else "Running"

    def _pop_rqm(self) -> RqmActionPlan:
        with self._lock:
            if self._scheduled_rqms:
                return self._scheduled_rqms.pop(0)
            else:
                return empty_action_plan


def _serialize_rqm_list(rqm_list: List[RqmActionPlan]) -> List[Dict]:
    rqm_serialized = [rqm.serialize() for rqm in rqm_list]
    return rqm_serialized
