from datetime import datetime
from typing import List

from waspy.iba.erd_entities import ErdRecipe, PositionCoordinates
from waspy.iba.erd_setup import ErdSetup
from waspy.iba.iba_error import RangeError


def run_erd_recipe(recipe: ErdRecipe, erd_setup: ErdSetup):
    start_time = datetime.now()
    erd_setup.move(PositionCoordinates(z=recipe.z_start, theta=recipe.theta))
    erd_setup.wait_for_arrival()
    erd_setup.configure_acquisition(recipe.measuring_time_sec, recipe.name)
    erd_setup.start_acquisition()
    erd_setup.wait_for_acquisition_started()
    z_range = get_z_range(recipe.z_start, recipe.z_end, recipe.z_increment, recipe.z_repeat)
    if len(z_range) == 0:
        raise RangeError("Invalid z range")
    wait_time = recipe.measuring_time_sec / len(z_range)
    for z in z_range:
        erd_setup.move(z)
        erd_setup.wait_for(wait_time)

    erd_setup.wait_for_acquisition_done()
    erd_setup.convert_data_to_ascii()
    return



def get_z_range(start, end, increment, repeat=1) -> List[PositionCoordinates]:
    if increment == 0:
        positions = [PositionCoordinates(z=start)]
    else:
        coordinate_range = np.arange(start, end + increment, increment)
        logging.info("start: " + str(start) + ", end: " + str(end) + ", inc: " + str(increment))
        numpy_z_steps = np.around(coordinate_range, decimals=2)
        positions = [PositionCoordinates(z=float(z_step)) for z_step in numpy_z_steps]

    repeated_positions = []
    [repeated_positions.extend(positions) for _ in range(repeat)]
    return repeated_positions
