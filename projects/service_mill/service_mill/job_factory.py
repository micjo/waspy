from erd_data_serializer import ErdDataSerializer
from erd_entities import ErdJobModel
from erd_job import ErdJob
from erd_setup import ErdSetup
from rbs_data_serializer import RbsDataSerializer
from rbs_entities import RbsJobModel
from rbs_job import RbsJob
from rbs_setup import RbsSetup


class RbsJobFactory:
    def __init__(self, setup: RbsSetup, data_serializer: RbsDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer

    def make_job(self, job_model: RbsJobModel):
        return RbsJob(job_model, self._setup, self._data_serializer)


class ErdJobFactory:
    def __init__(self, setup: ErdSetup, data_serializer: ErdDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer

    def make_job(self, job_model: ErdJobModel):
        return ErdJob(job_model, self._setup, self._data_serializer)
