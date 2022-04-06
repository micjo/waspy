from erd_data_serializer import ErdDataSerializer
from erd_entities import ErdJobModel
from erd_job import ErdJob
from erd_setup import ErdSetup
from rbs_data_serializer import RbsDataSerializer
from rbs_entities import RbsJobModel
from rbs_job import RbsJob
import rbs_random_csv_to_json
import erd_csv_to_json
from rbs_setup import RbsSetup


class RbsJobFactory:
    def __init__(self, setup: RbsSetup, data_serializer: RbsDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer

    def make_job(self, job_model: RbsJobModel):
        return RbsJob(job_model, self._setup, self._data_serializer)

    def make_job_model_from_csv(self, contents):
        top_section, detectors_section, recipes_section = rbs_random_csv_to_json.get_sections(contents)
        settings = rbs_random_csv_to_json.parse_top_settings(top_section)
        settings["detectors"] = rbs_random_csv_to_json.parse_list_settings(detectors_section)
        settings["recipes"] = rbs_random_csv_to_json.parse_recipes(recipes_section)
        self._setup.verify_caen_boards(settings["detectors"])
        return RbsJobModel.parse_obj(settings)


class ErdJobFactory:
    def __init__(self, setup: ErdSetup, data_serializer: ErdDataSerializer):
        self._setup = setup
        self._data_serializer = data_serializer

    def make_job(self, job_model: ErdJobModel):
        return ErdJob(job_model, self._setup, self._data_serializer)

    def make_job_model_from_csv(self, contents):
        return erd_csv_to_json.parse_rqm(contents)

