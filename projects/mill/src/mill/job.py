import logging
from typing import Dict

from mill.mill_error import MillError
from waspy.iba.iba_error import IbaError, CancelError
from waspy.drivers.driver_error import DriverError


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

    def cancel(self):
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

    def cancel(self):
        pass


empty_job = EmptyJob()


def execute(job: Job):
    job.setup()
    logging.info("[JOB] start: " + str(job.serialize()))
    try:
        job.exec()
        job.teardown()
    except (CancelError, DriverError, IbaError, MillError) as e:
        job.terminate(str(e))
        return

