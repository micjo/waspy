import time
from typing import List
import copy

from app.rbs_experiment.entities import RbsRqmSettings, RbsRqmStatus, RbsRqmRandom, RbsRqmChanneling, \
    RbsRqmMinimizeYield, RbsRqmFixed, RecipeType, PositionCoordinates
import app.rbs_experiment.rbs as rbs_lib
import app.rbs_experiment.yield_plot as plot


def make_count_callback(rbs_rqm_status: RbsRqmStatus):
    counts_at_start = rbs_rqm_status.accumulated_charge

    def count_callback(counter_data):
        charge = float(counter_data["charge(nC)"])
        target_charge = float(counter_data["target_charge(nC)"])
        if charge < target_charge:
            rbs_rqm_status.accumulated_charge = counts_at_start + charge
        else:
            rbs_rqm_status.accumulated_charge = counts_at_start + target_charge

    return count_callback


def minimize_yield(settings: RbsRqmSettings, rbs: rbs_lib.Rbs, status: RbsRqmStatus, recipe: RbsRqmMinimizeYield):
    rbs.move(recipe.start_position)
    positions = rbs_lib.get_position_range(recipe.vary_coordinate)
    rbs.prepare_counting(recipe.total_charge / len(positions))

    detector_optimize = settings.detectors[recipe.optimize_detector_index]
    energy_yields = []

    for position in positions:
        start = time.time()
        rbs.prepare_data_acquisition()
        rbs.move_and_count(position, make_count_callback(status))
        data = rbs.get_packed_histogram(detector_optimize)
        integrated_energy_yield = rbs_lib.get_sum(data, recipe.integration_window)
        energy_yields.append(integrated_energy_yield)
        run_time = time.time() - start
        file_stem = recipe.file_stem + "_" + rbs_lib.single_coordinate_to_string(position, recipe.vary_coordinate)
        total_charge = rbs.get_charge()
        rbs.flush_histograms(settings, recipe.sample_id, file_stem, run_time, total_charge)

    min_position = rbs_lib.get_minimum_yield_position(settings.rqm_number, recipe, positions, energy_yields)
    rbs.move(min_position)


def run_random(settings: RbsRqmSettings, rbs: rbs_lib.Rbs, status: RbsRqmStatus, recipe: RbsRqmRandom):
    rbs.move(recipe.start_position)
    positions = rbs_lib.get_position_range(recipe.vary_coordinate)
    rbs.prepare_counting(recipe.charge_total / len(positions))
    rbs.prepare_data_acquisition()

    start = time.time()

    total_charge = 0
    for index, position in enumerate(positions):
        rbs.move_and_count(position, make_count_callback(status))
        total_charge += rbs.get_charge()

    end = time.time()
    run_time = end - start
    random_histograms = rbs.flush_histograms(settings, recipe.sample_id, recipe.file_stem, run_time, total_charge)
    rbs.stop_data_acquisition()
    return random_histograms


def run_fixed(settings: RbsRqmSettings, rbs: rbs_lib.Rbs, status: RbsRqmStatus, recipe: RbsRqmFixed):
    start = time.time()
    rbs.prepare_counting(recipe.charge_total)
    rbs.prepare_data_acquisition()

    rbs.count(make_count_callback(status))
    end = time.time()
    run_time = end - start

    total_charge = rbs.get_charge()
    fixed_histograms = rbs.flush_histograms(settings, recipe.sample_id, recipe.file_stem, run_time, total_charge)
    return fixed_histograms


def run_channeling(settings: RbsRqmSettings, rbs: rbs_lib.Rbs, status: RbsRqmStatus, recipe: RbsRqmChanneling):
    rbs.move(recipe.start_position)
    for index, vary_coordinate in enumerate(recipe.yield_vary_coordinates):
        yield_recipe = RbsRqmMinimizeYield(type=RecipeType.minimize_yield, sample_id=recipe.sample_id,
                                           file_stem=recipe.file_stem + str(index),
                                           total_charge=recipe.yield_charge_total,
                                           vary_coordinate=vary_coordinate, integration_window=
                                           recipe.yield_integration_window,
                                           optimize_detector_index=recipe.yield_optimize_detector_index)
        yield_folder = settings.rqm_number + "/" + recipe.file_stem + "_" + str(index) + "_vary_" + str(
            vary_coordinate.name)
        await minimize_yield_for_positions(yield_folder, yield_recipe, detectors, rbs_rqm_status)

    fixed_recipe = entities.RbsRqmFixed(type=entities.RecipeType.fixed, sample_id=recipe.sample_id,
                                        file_stem=recipe.file_stem + "_fixed",
                                        charge_total=recipe.random_fixed_charge_total)
    fixed_histograms = await run_fixed(sub_folder, fixed_recipe, detectors, rbs_rqm_status)
    fixed_labels = [detector.identifier + "_fixed" for detector in detectors]

    random_recipe = entities.RbsRqmRandom(type=entities.RecipeType.random, sample_id=recipe.sample_id,
                                          file_stem=recipe.file_stem + "_random",
                                          charge_total=recipe.random_fixed_charge_total,
                                          start_position={"theta": -2}, vary_coordinate=recipe.random_vary_coordinate)
    random_histograms = await run_random(sub_folder, random_recipe, detectors, rbs_rqm_status)
    random_labels = [detector.identifier + "_random" for detector in detectors]

    plot.plot_compare(sub_folder, recipe.file_stem, fixed_histograms, fixed_labels, random_histograms, random_labels)


def get_total_counts_random(recipe: entities.RbsRqmRandom):
    return recipe.charge_total


def get_total_counts_channeling(recipe: entities.RbsRqmChanneling):
    yield_optimize_total_charge = recipe.yield_charge_total * len(recipe.yield_vary_coordinates)
    compare_total_charge = 2 * recipe.random_fixed_charge_total
    return yield_optimize_total_charge + compare_total_charge


def run_recipe_list(rbs_setup: rbs_lib.Rbs, rbs_rqm: entities.RbsRqm):
    rbs_rqm.status.run_status = entities.StatusModel.Running
    rbs_rqm.status.rqm = rbs_rqm

    for recipe in rbs_rqm.recipes:
        rbs_rqm.status.accumulated_charge = 0
        rbs_rqm.status.accumulated_charge_target = 0
        rbs_rqm.status.active_recipe = recipe.sample_id

        if recipe.type == entities.RecipeType.channeling:
            rbs_rqm.status.accumulated_charge_target = get_total_counts_channeling(recipe)
            run_channeling(rbs_rqm.settings, recipe, rbs_rqm.status)
        if recipe.type == entities.RecipeType.random:
            rbs_rqm.status.accumulated_charge_target = get_total_counts_random(recipe)
            run_random(rbs_rqm.settings, rbs_setup, rbs_rqm.status, recipe)

    rbs_rqm.status.run_status = entities.StatusModel.Idle
    rbs_rqm.status.active_recipe = ""
    rbs_rqm.status.accumulated_charge = 0
    rbs_rqm.status.accumulated_charge_target = 0
