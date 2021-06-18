import time
from typing import List

import app.rbs_experiment.entities as rbs
import app.rbs_experiment.daemon_control as control
import app.rbs_experiment.plotting as plot


async def run_minimize_yield(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel],
                             rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.sample_id, recipe.start_position)
    positions = await control.get_position_range(recipe)
    await control.prepare_counting(recipe.sample_id, recipe.total_charge / len(positions))

    detector_optimize = detectors[recipe.optimize_detector_index]
    energy_yields = []

    for position in positions:
        run_time = await run_minimize_yield_step(position, detector_optimize, energy_yields, recipe)
        file_stem = recipe.file_stem + "_" + control.single_coordinate_to_string(position, recipe.vary_coordinate)
        await control.get_and_save_histograms(sub_folder, file_stem, recipe.sample_id, run_time, detectors)

    min_position = await control.get_minimum_yield_position(sub_folder, recipe, positions, energy_yields)
    await control.move_to_position(recipe.sample_id + "_move_to_min_position", min_position)


async def run_minimize_yield_step(position: rbs.PositionCoordinates, detector_optimize, energy_yields, recipe):
    start = time.time()

    recipe_id = recipe.sample_id + "_" + control.single_coordinate_to_string(position, recipe.vary_coordinate)

    await control.prepare_data_acquisition(recipe_id)
    await control.move_position_and_count(recipe_id, position)
    data = await control.get_packed_histogram(detector_optimize)
    integrated_energy_yield = control.get_sum(data, recipe.integration_window)
    energy_yields.append(integrated_energy_yield)

    end = time.time()
    return end - start


async def run_random(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel],
                     rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.sample_id, recipe.start_position)
    positions = await control.get_position_range(recipe)
    await control.prepare_counting(recipe.sample_id, recipe.total_charge / len(positions))
    await control.prepare_data_acquisition(recipe.sample_id)

    start = time.time()
    for position in positions:
        await control.move_position_and_count(recipe.sample_id + "_" + str(position), position)
    end = time.time()
    run_time_msec = end - start
    random_histograms = await control.get_and_save_histograms(sub_folder, recipe.file_stem, recipe.sample_id,
                                                              run_time_msec, detectors)
    return random_histograms


async def run_fixed(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel],
                    rbs_rqm_status: rbs.RbsRqmStatus):
    start = time.time()
    await control.prepare_counting(recipe.sample_id + "pause_set", recipe.total_charge)
    await control.prepare_data_acquisition(recipe.sample_id)
    await control.move_position_and_count(recipe.sample_id + "move_acquire", recipe.start_position)
    end = time.time()
    measuring_time_msec = end - start

    fixed_histograms = await control.get_and_save_histograms(sub_folder, recipe.file_stem, recipe.sample_id,
                                                             measuring_time_msec, detectors)
    return fixed_histograms


async def run_fixed_random_compare(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel],
                                   rbs_rqm_status: rbs.RbsRqmStatus):
    original_stem = recipe.file_stem

    recipe.file_stem += original_stem + "_fixed"
    fixed_histograms = await run_fixed(sub_folder, recipe, detectors, rbs_rqm_status)

    recipe.file_stem += original_stem + "_random"
    random_histograms = await run_random(sub_folder, recipe, detectors, rbs_rqm_status)

    total_histograms = len(fixed_histograms)

    for i in range(0, total_histograms):
        plot.append_histogram_plot("fixed_" + detectors[i].identifier, fixed_histograms[i], total_histograms, i)
        plot.append_histogram_plot("random_" + detectors[i].identifier, random_histograms[i], total_histograms, i)


async def run_recipe_list(rbs_rqm: rbs.RbsRqm, rbs_rqm_status: rbs.RbsRqmStatus):
    sub_folder = rbs_rqm.rqm_number

    rbs_rqm_status.run_status = rbs.StatusModel.Running
    rbs_rqm_status.rqm = rbs_rqm

    for recipe in rbs_rqm.recipes:
        rbs_rqm_status.active_recipe = recipe.sample_id
        rbs_rqm_status.recipe_progress_percentage = 0

        if recipe.type == rbs.RecipeType.minimize_yield:
            await run_minimize_yield(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)
        if recipe.type == rbs.RecipeType.random:
            await run_random(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)
        if recipe.type == rbs.RecipeType.fixed_random_compare:
            await run_fixed_random_compare(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)

    rbs_rqm_status.run_status = rbs.StatusModel.Parking
    await control.move_to_position(rbs_rqm.rqm_number + "_parking", rbs_rqm.parking_position)

    rbs_rqm_status.run_status = rbs.StatusModel.Idle
