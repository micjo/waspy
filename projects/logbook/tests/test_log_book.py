from logbook.sqlite_db import SqliteDb
from logbook.make_db import make_imec_db
from pathlib import Path
import os
from datetime import datetime, timedelta
from logbook.entities import RbsSingleStepRecipe, RbsRecipeType, RbsStepwiseRecipe, RbsStepwiseLeastRecipe

import unittest


class TestDbTables(unittest.TestCase):
    def setUp(self):
        file = Path("test.db")
        file.unlink(missing_ok=True)
        make_imec_db("test.db")
        self.db = SqliteDb(file)

    def tearDown(self):
        pass
        # file = Path("test.db")
        # file.unlink(missing_ok=True)

    def test_log_message(self):
        self.db.log_message("message", "this is a test", datetime.now())
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "this is a test")

    def test_log_job(self):
        self.db.log_job_start("test_job")
        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job started")
        assert (messages[0]["mode"] == "job")

    def test_log_job_with_3_recipes(self):
        self.db.log_job_start("test_job")

        start_time = datetime.now()
        end_time = datetime.now() + timedelta(hours=1)

        rbs_recipe_1 = RbsSingleStepRecipe(type=RbsRecipeType.SINGLE_STEP, sample="sample_001", recipe="recipe_001",
                                           start_time=start_time, end_time=end_time, axis="x", position=17.5)
        rbs_recipe_2 = RbsStepwiseRecipe(type=RbsRecipeType.STEPWISE, sample="sample_002", recipe="recipe_003",
                                         start_time=start_time, end_time=end_time, vary_axis="x", start=0, end=30,
                                         step=2)
        rbs_recipe_3 = RbsStepwiseLeastRecipe(type=RbsRecipeType.STEPWISE_LEAST, sample="sample_003",
                                              recipe="recipe_003", start_time=start_time, end_time=end_time,
                                              vary_axis="x", start=0, end=30, step=2, least_yield_position=-1.3,
                                              yield_positions=[(-2.0, 50), (-1.8, 100)])

        self.db.log_rbs_recipe(rbs_recipe_1)
        self.db.log_rbs_recipe(rbs_recipe_2)
        self.db.log_rbs_recipe(rbs_recipe_3)

        messages = self.db.get_log_messages()
        assert (messages[0]["note"] == "test_job started")

        print(self.db.get_log_messages())
        print(self.db.get_angle_yields(messages[3]["recipe_id"]))
