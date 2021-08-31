import time
from typing import List

import app.rbs_experiment.entities as rbs
import app.rbs_experiment.hw_procedures as control
import app.rbs_experiment.yield_plot as plot


def make_count_callback(rbs_rqm_status: rbs.RbsRqmStatus):
    counts_at_start = rbs_rqm_status.accumulated_charge

    def count_callback(counter_data):
        charge = float(counter_data["charge(nC)"])
        target_charge = float(counter_data["target_charge(nC)"])
        if charge < target_charge:
            rbs_rqm_status.accumulated_charge = counts_at_start + charge
        else:
            rbs_rqm_status.accumulated_charge = counts_at_start + target_charge

    return count_callback


async def minimize_yield_for_positions(sub_folder, recipe: rbs.RbsRqmMinimizeYield,
                                       detectors: List[rbs.CaenDetectorModel],
                                       rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.sample_id, recipe.start_position)
    positions = await control.get_position_range(recipe.vary_coordinate)
    await control.prepare_counting(recipe.sample_id, recipe.total_charge / len(positions))

    detector_optimize = detectors[recipe.optimize_detector_index]
    energy_yields = []

    for position in positions:
        start = time.time()
        integrated_energy_yield = await integrate_yield_for_position(position, detector_optimize, recipe,
                                                                     rbs_rqm_status)
        energy_yields.append(integrated_energy_yield)
        run_time = time.time() - start
        file_stem = recipe.file_stem + "_" + control.single_coordinate_to_string(position, recipe.vary_coordinate)
        total_charge = control.get_charge()
        await control.get_and_save_histograms(sub_folder, file_stem, recipe.sample_id, run_time, total_charge,
                                              detectors)

    min_position = await control.get_minimum_yield_position(sub_folder, recipe, positions, energy_yields)
    await control.move_to_position(recipe.sample_id + "_move_to_min_position", min_position)


async def integrate_yield_for_position(position: rbs.PositionCoordinates, detector_optimize,
                                       recipe: rbs.RbsRqmMinimizeYield, rbs_rqm_status: rbs.RbsRqmStatus):
    recipe_id = recipe.sample_id + "_" + control.single_coordinate_to_string(position, recipe.vary_coordinate)

    await control.prepare_data_acquisition(recipe_id)

    await control.move_position_and_count(recipe_id, position, make_count_callback(rbs_rqm_status))
    data = await control.get_packed_histogram(detector_optimize)
    integrated_energy_yield = control.get_sum(data, recipe.integration_window)

    return integrated_energy_yield


async def run_random(sub_folder, recipe: rbs.RbsRqmRandom, detectors: List[rbs.CaenDetectorModel],
                     rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.sample_id, recipe.start_position)
    positions = await control.get_position_range(recipe.vary_coordinate)
    await control.prepare_counting(recipe.sample_id, recipe.charge_total / len(positions))
    await control.prepare_data_acquisition(recipe.sample_id)

    start = time.time()

    total_charge = 0
    for index, position in enumerate(positions):
        await control.move_position_and_count(recipe.sample_id + "_" + str(position), position,
                                              make_count_callback(rbs_rqm_status))
        total_charge += await control.get_charge()

    end = time.time()
    run_time_msec = end - start
    random_histograms = await control.get_and_save_histograms(sub_folder, recipe.file_stem, recipe.sample_id,
                                                              run_time_msec, total_charge, detectors)
    return random_histograms


async def run_fixed(sub_folder, recipe: rbs.RbsRqmFixed, detectors: List[rbs.CaenDetectorModel],
                    rbs_rqm_status: rbs.RbsRqmStatus):
    start = time.time()
    await control.prepare_counting(recipe.sample_id + "pause_set", recipe.charge_total)
    await control.prepare_data_acquisition(recipe.sample_id)

    await control.count(recipe.sample_id + "count", make_count_callback(rbs_rqm_status))
    end = time.time()
    measuring_time_msec = end - start

    total_charge = control.get_charge()
    fixed_histograms = await control.get_and_save_histograms(sub_folder, recipe.file_stem, recipe.sample_id,
                                                             measuring_time_msec, total_charge, detectors)
    return fixed_histograms


async def run_channeling(sub_folder, recipe: rbs.RbsRqmChanneling, detectors: List[rbs.CaenDetectorModel],
                         rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.sample_id, recipe.start_position)
    for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
        yield_recipe = rbs.RbsRqmMinimizeYield(type=rbs.RecipeType.minimize_yield, sample_id=recipe.sample_id,
                                               file_stem=recipe.file_stem + str(index),
                                               total_charge=recipe.yield_charge_total,
                                               vary_coordinate=vary_coordinate, integration_window=
                                               recipe.yield_integration_window,
                                               optimize_detector_index=recipe.yield_optimize_detector_index)
        yield_folder = sub_folder + "/" + recipe.file_stem + "_" + str(index) + "_vary_" + str(vary_coordinate.name)
        await minimize_yield_for_positions(yield_folder, yield_recipe, detectors, rbs_rqm_status)

    fixed_recipe = rbs.RbsRqmFixed(type=rbs.RecipeType.fixed, sample_id=recipe.sample_id,
                                   file_stem=recipe.file_stem + "_fixed", charge_total=recipe.random_fixed_charge_total)
    fixed_histograms = await run_fixed(sub_folder, fixed_recipe, detectors, rbs_rqm_status)
    fixed_labels = [detector.identifier + "_fixed" for detector in detectors]

    random_recipe = rbs.RbsRqmRandom(type=rbs.RecipeType.random, sample_id=recipe.sample_id,
                                     file_stem=recipe.file_stem + "_random",
                                     charge_total=recipe.random_fixed_charge_total,
                                     start_position={"theta": -2}, vary_coordinate=recipe.random_vary_coordinate)
    random_histograms = await run_random(sub_folder, random_recipe, detectors, rbs_rqm_status)
    random_labels = [detector.identifier + "_random" for detector in detectors]

    plot.plot_compare(sub_folder, recipe.file_stem, fixed_histograms, fixed_labels, random_histograms, random_labels)


def get_total_counts_random(recipe: rbs.RbsRqmRandom):
    return recipe.charge_total


def get_total_counts_channeling(recipe: rbs.RbsRqmChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_vary_coordinates)
    compare_total_charge = 2 * recipe.random_fixed_charge_total
    return yield_optimize_total_charge + compare_total_charge

def make_test_recipe(recipe: rbs.RbsRqmRandom):
    """ Verify that the caen acquisition is properly cleared """
    mini_recipe = recipe
    mini_recipe.file_stem += "_TEST"
    mini_recipe.charge_total = 2000
    mini_recipe.vary_coordinate = rbs.VaryCoordinate(name="phi", start=0, end=0, increment=0)
    return mini_recipe


async def run_recipe_list(rbs_rqm: rbs.RbsRqm, rbs_rqm_status: rbs.RbsRqmStatus):
    sub_folder = rbs_rqm.rqm_number

    rbs_rqm_status.run_status = rbs.StatusModel.Running
    rbs_rqm_status.rqm = rbs_rqm

    for recipe in rbs_rqm.recipes:
        if recipe.type == rbs.RecipeType.move:
            await control.move_to_position(rbs_rqm.rqm_number + "_move", recipe.position)
            continue

        rbs_rqm_status.active_recipe = recipe.sample_id

        if recipe.type == rbs.RecipeType.channeling:
            rbs_rqm_status.accumulated_charge_target = get_total_counts_channeling(recipe)
            await run_channeling(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)
        if recipe.type == rbs.RecipeType.random:
            test_histogram_recipe = make_test_recipe(recipe)
            rbs_rqm_status.accumulated_charge_target = get_total_counts_random(test_histogram_recipe)
            rbs_rqm_status.accumulated_charge_target += get_total_counts_random(recipe)
            await run_random(sub_folder, test_histogram_recipe, rbs_rqm.detectors, rbs_rqm_status)
            await run_random(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)

    rbs_rqm_status.run_status = rbs.StatusModel.Idle
    rbs_rqm_status.accumulated_charge = 0
    rbs_rqm_status.accumulated_charge_target = 0
    rbs_rqm_status.active_recipe = ""
