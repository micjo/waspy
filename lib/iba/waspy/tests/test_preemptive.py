import unittest
import time
from threading import Thread
from waspy.iba.preempt import preemptive


class SlowCall(object):
    _cancel: bool

    def __init__(self):
        self._cancel = False

    @preemptive
    def wait(self):
        for _ in range(10):
            print("SlowCall.wait")
            time.sleep(1)
            yield


class TestAsyncCancel(unittest.TestCase):
    def test_cancel(self):
        slow_call = SlowCall()
        t1 = Thread(target=slow_call.wait)
        t1.start()
        time.sleep(2)
        slow_call._cancel = True
        t1.join()


