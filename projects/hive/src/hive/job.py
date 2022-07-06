import logging
from typing import Dict, Generator

from waspy.hardware_control.hive_exception import AbortedError, HiveError
from waspy.hardware_control.http_helper import HardwareError


class Job:
    def setup(self) -> None:
        raise NotImplementedError("")

    def exec(self) -> None:
        raise NotImplementedError("")

    def teardown(self) -> None:
        raise NotImplementedError("")

    def terminate(self, message: str) -> None:
        raise NotImplementedError("")

    def serialize(self) -> Dict:
        raise NotImplementedError("")

    def abort(self):
        raise NotImplementedError("")


class EmptyJob(Job):
    def setup(self) -> Dict:
        pass

    def exec(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def terminate(self, message: str) -> None:
        pass

    def serialize(self) -> Dict:
        return {}

    def abort(self):
        pass


empty_job = EmptyJob()


def execute(job: Job):
    job.setup()
    logging.info("[JOB] start: " + str(job.serialize()))
    try:
        job.exec()
        job.teardown()
    except (AbortedError, HardwareError, HiveError) as e:
        job.terminate(str(e))
        return

