from app.erd.entities import ErdRqm, Erd, PositionCoordinates
from app.erd.erd_hardware import ErdSetup, get_z_range
from hive_exception import HiveError


def run_recipe(recipe: Erd, erd_setup: ErdSetup):
    erd_setup.move(PositionCoordinates(z=recipe.z_min, theta=recipe.theta))
    erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.spectrum_filename)
    erd_setup.start_acquisition()
    for z in get_z_range(recipe.z_min, recipe.z_max, recipe.z_increment):
        erd_setup.move(z)
    erd_setup.wait_for_acquisition_done()


def run_erd_rqm(self, erd_rqm: ErdRqm, erd_setup: ErdSetup):
    try:
        for recipe in erd_rqm.recipes:
            run_recipe(recipe, erd_setup)
    except HiveError as e:
        self.error = e
