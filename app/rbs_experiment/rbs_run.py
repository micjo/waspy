import time
from typing import List

import numpy as np

import app.rbs_experiment.entities as rbs
import app.rbs_experiment.fitting as fit
import app.rbs_experiment.daemon_control as control
import app.rbs_experiment.plotting as plot
import app.rbs_experiment.storing as store


async def run_pre_channeling(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel],
                             rbs_rqm_status: rbs.RbsRqmStatus):
    await control.move_to_position(recipe.title, recipe.start_position)
    angle_values = control.make_coordinate_range(recipe.vary_coordinate)
    angle_to_vary = recipe.vary_coordinate.name

    charge_limit_per_step = recipe.total_charge / len(angle_values)
    await control.counting_pause_and_set_target(recipe.title, charge_limit_per_step)
    detector_optimize = detectors[recipe.optimize_detector_index]
    active_detectors = [detectors[index] for index in recipe.detector_indices]

    energy_yields = []
    for index, angle in enumerate(angle_values):

        rbs_rqm_status.recipe_progress_percentage = round(index / len(angle_values) * 100, 2)
        start = time.time()
        await control.stop_clear_and_arm_caen_acquisition(recipe.title)
        await control.move_to_angle_then_acquire_till_target(recipe.title + "_" + str(angle), angle_to_vary, angle)
        data = await control.get_packed_histogram(detector_optimize)
        integrated_energy_yield = control.get_sum(data, recipe.integration_window)
        energy_yields.append(integrated_energy_yield)
        end = time.time()
        measuring_time_msec = end - start
        file_stem = recipe.file_stem + "_" + angle_to_vary + "_" + str(angle)

        for detector in active_detectors:
            data = await control.get_packed_histogram(detector)
            await store.store_histogram(sub_folder, file_stem, detector.identifier, measuring_time_msec, recipe.title,
                                        data)
            plot.append_histogram_plot(detector, data)
        plot.store_histogram_plot_and_clear(sub_folder, file_stem)

    store.store_yields(sub_folder, recipe.file_stem, angle_values, energy_yields)

    smooth_angles, smooth_yields = fit.fit_and_smooth(angle_values, energy_yields)
    plot.plot_energy_yields_and_clear(sub_folder, recipe.file_stem, angle_values, energy_yields, smooth_angles,
                                      smooth_yields, angle_to_vary)
    index_for_minimum_yield = np.argmin(smooth_yields)
    min_angle = round(smooth_angles[index_for_minimum_yield], 2)

    await control.move_to_angle(recipe.title + "_move_to_min_angle", angle_to_vary, min_angle)


async def run_random(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel]):
    start = time.time()
    await control.move_to_position(recipe.title, recipe.start_position)
    angle_values = control.make_coordinate_range(recipe.vary_coordinate)
    angle_to_vary = recipe.vary_coordinate.name

    charge_limit_per_step = recipe.total_charge / len(angle_values)
    await control.counting_pause_and_set_target(recipe.title, charge_limit_per_step)
    await control.stop_clear_and_arm_caen_acquisition(recipe.title)

    for angle in angle_values:
        await control.move_to_angle_then_acquire_till_target(recipe.title + "_" + str(angle), angle_to_vary, angle)
    end = time.time()
    measuring_time_msec = end - start

    active_detectors = [detectors[index] for index in recipe.detector_indices]
    for detector in active_detectors:
        data = await control.get_packed_histogram(detector)
        await store.store_histogram(sub_folder, recipe.file_stem, detector.identifier, measuring_time_msec,
                                    recipe.title, data)
        plot.append_histogram_plot(detector, data)
    plot.store_histogram_plot_and_clear(sub_folder, recipe.file_stem)


async def run_channeling(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[rbs.CaenDetectorModel]):
    start = time.time()

    await control.move_to_position(recipe.title, recipe.start_position)
    await control.counting_pause_and_set_target(recipe.title, recipe.total_charge)
    await control.stop_clear_and_arm_caen_acquisition(recipe.title)

    end = time.time()
    measuring_time_msec = end - start

    active_detectors = [detectors[index] for index in recipe.detector_indices]
    for detector in active_detectors:
        data = await control.get_packed_histogram(detector)
        await store.store_histogram(sub_folder, recipe.file_stem, detector.identifier, measuring_time_msec,
                                    recipe.title, data)
        plot.append_histogram_plot(detector, data)
    plot.store_histogram_plot_and_clear(sub_folder, recipe.file_stem)


async def run_recipe_list(rbs_rqm: rbs.RbsRqm, rbs_rqm_status: rbs.RbsRqmStatus):
    sub_folder = rbs_rqm.rqm_number

    rbs_rqm_status.run_status = rbs.StatusModel.Running
    rbs_rqm_status.rqm = rbs_rqm

    for recipe in rbs_rqm.recipes:
        rbs_rqm_status.active_recipe = recipe.title
        rbs_rqm_status.recipe_progress_percentage = 0
        if recipe.type == rbs.RecipeType.pre_channeling:
            await run_pre_channeling(sub_folder, recipe, rbs_rqm.detectors, rbs_rqm_status)
        if recipe.type == rbs.RecipeType.random:
            await run_random(sub_folder, recipe, rbs_rqm.detectors)
        if recipe.type == rbs.RecipeType.channeling:
            await run_channeling(sub_folder, recipe, rbs_rqm.detectors)

    rbs_rqm_status.run_status = rbs.StatusModel.Parking
    await control.move_to_position(rbs_rqm.rqm_number + "_parking", rbs_rqm.parking_position)

    rbs_rqm_status.run_status = rbs.StatusModel.Idle
