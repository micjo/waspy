from typing import Literal

from logbook.sqlite_db import SqliteDb
from logbook.make_db import make_imec_db
from pathlib import Path
import os
from datetime import datetime, timedelta
from logbook.entities import RbsSingleStepRecipe, RbsRecipeType, RbsStepwiseRecipe, RbsStepwiseLeastRecipe, \
    ErdRecipeModel

import unittest


class TestDbTables(unittest.TestCase):
    def setUp(self):
        file = Path("test.db")
        file.unlink(missing_ok=True)
        make_imec_db("test.db")
        self.db = SqliteDb(file)

    def tearDown(self):
        file = Path("test.db")
        file.unlink(missing_ok=True)

    def test_log_message(self):
        self.db._add_to_logbook("message", "this is a test", datetime.now())
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "this is a test")

    def test_log_job(self):
        self.db.log_job_start("test_job")
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job started")
        assert (messages[0]["mode"] == "job")

    def test_log_finished(self):
        self.db.log_job_finish("test_job")
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job finished")
        assert (messages[0]["mode"] == "job")

    def test_job_terminated(self):
        self.db.log_job_terminated("test_job", "daemon did not respond")
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job terminated: daemon did not respond")
        assert (messages[0]["mode"] == "job")

    def test_log_rbs_job_with_3_recipes(self):
        self.db.log_job_start("test_job")
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(hours=1)

        rbs_recipe_1 = RbsSingleStepRecipe(sample="sample_001", name="recipe_001",
                                           start_time=start_time, end_time=end_time, axis="x", position=17.5)
        rbs_recipe_2 = RbsStepwiseRecipe(sample="sample_002", name="recipe_002",
                                         start_time=start_time, end_time=end_time, vary_axis="x", start=0, end=30,
                                         step=2)
        rbs_recipe_3 = RbsStepwiseLeastRecipe(sample="sample_003",
                                              name="recipe_003", start_time=start_time, end_time=end_time,
                                              vary_axis="x", start=0, end=30, step=2, least_yield_position=-1.3,
                                              yield_positions=[(-2.0, 50), (-1.8, 100)])

        self.db.log_recipe_finished(rbs_recipe_1)
        self.db.log_recipe_finished(rbs_recipe_2)
        self.db.log_recipe_finished(rbs_recipe_3)
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job started")
        assert (messages[1]["note"] == "recipe_001 finished")
        assert (messages[1]["move"] == "")
        assert (messages[2]["note"] == "recipe_002 finished")
        assert (messages[2]["move"] == "x: [0.0,30.0,2.0]")
        assert (messages[3]["note"] == "recipe_003 finished")
        assert (messages[3]["move"] == "x: [0.0,30.0,2.0]-> -1.3")
        assert (self.db.get_angle_yields(messages[3]["recipe_id"]) == [{'angle': -2.0, "yield": 50},
                                                                       {"angle": -1.8, "yield": 100}])

    def test_log_erd_job_with_3_recipes(self):
        self.db.log_job_start("test_job")
        erd_recipe_1 = ErdRecipeModel(beam_type="Cl4+", beam_energy_MeV="8.5", sample_tilt_degrees="2.1",
                                      sample="sample_erd_001", name="recipe_erd_001", measuring_time_sec="1200",
                                      theta=45.0, z_start=50, z_end=70, z_increment=2, z_repeat=2,
                                      start_time=datetime.now(), end_time=datetime.now() + timedelta(hours=1),
                                      average_terminal_voltage=-100)
        erd_recipe_2 = ErdRecipeModel(beam_type="Cl4+", beam_energy_MeV="8.5", sample_tilt_degrees="2.1",
                                      sample="sample_erd_002", name="recipe_erd_002", measuring_time_sec="1200",
                                      theta=45.0, z_start=40, z_end=50, z_increment=2, z_repeat=1,
                                      start_time=datetime.now(), end_time=datetime.now() + timedelta(hours=1),
                                      average_terminal_voltage=-100)
        erd_recipe_3 = ErdRecipeModel(beam_type="Cl4+", beam_energy_MeV="8.5", sample_tilt_degrees="2.1",
                                      sample="sample_erd_003", name="recipe_erd_003", measuring_time_sec="1200",
                                      theta=45.0, z_start=20, z_end=40, z_increment=2, z_repeat=4,
                                      start_time=datetime.now(), end_time=datetime.now() + timedelta(hours=1),
                                      average_terminal_voltage=-100)
        self.db.log_recipe_finished(erd_recipe_1)
        self.db.log_recipe_finished(erd_recipe_2)
        self.db.log_recipe_finished(erd_recipe_3)
        messages = self.db.get_log_messages()
        assert (messages[1]["note"] == "recipe_erd_001 finished")
        assert (messages[1]["move"] == "Z: [50.0,70.0,2.0] *2")
        assert (messages[1]["recipe_name"] == "recipe_erd_001")

        assert (messages[2]["note"] == "recipe_erd_002 finished")
        assert (messages[2]["recipe_name"] == "recipe_erd_002")
        assert (messages[2]["move"] == "Z: [40.0,50.0,2.0] *1")

        assert (messages[3]["recipe_name"] == "recipe_erd_003")
        assert (messages[3]["move"] == "Z: [20.0,40.0,2.0] *4")

    def test_failed_recipe(self):
        self.db.log_job_start("test_job")
        start_time = datetime.now()
        end_time = datetime.now() + timedelta(hours=1)

        rbs_recipe_1 = RbsStepwiseLeastRecipe(sample="sample_001",
                                              name="recipe_001", start_time=start_time, end_time=end_time,
                                              vary_axis="x", start=0, end=30, step=2, least_yield_position=-1.3,
                                              yield_positions=[(-2.0, 50), (-1.8, 100)])
        self.db.log_recipe_terminated(rbs_recipe_1, "fitting fail")
        messages = self.db.get_log_messages()
        assert (messages[1]["note"] == "recipe_001 failed: fitting fail")


