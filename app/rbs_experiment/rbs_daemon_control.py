import math

import app.hardware_controllers.daemon_comm as comm
from app.rbs_experiment.entities import PositionCoordinates, VaryCoordinate, CoordinateEnum, CaenDetectorModel, Window
from app.setup.config import daemons, output_dir, output_dir_remote
from typing import List
import app.rbs_experiment.py_fitter as fit

import app.rbs_experiment.entities as rbs
import logging
import numpy as np
import matplotlib.pyplot as plt
import traceback
import datetime
import asyncio
import time
from shutil import copy2
from pathlib import Path


async def move_to_position(identifier: str, position: PositionCoordinates):
    logging.info("Moving rbs system to '" + str(position) + "'")
    print("Moving rbs system to '" + str(position) + "'")

    if position is None:
        return
    if position.x is not None:
        await comm.move_aml_first(identifier, daemons.aml_x_y.url, position.x)
    if position.y is not None:
        await comm.move_aml_second(identifier, daemons.aml_x_y.url, position.y)
    if position.phi is not None:
        await comm.move_aml_first(identifier, daemons.aml_phi_zeta.url, position.phi)
    if position.zeta is not None:
        await comm.move_aml_second(identifier, daemons.aml_phi_zeta.url, position.zeta)
    if position.detector is not None:
        await comm.move_aml_first(identifier, daemons.aml_det_theta.url, position.detector)
    if position.theta is not None:
        await comm.move_aml_second(identifier, daemons.aml_det_theta.url, position.theta)


async def move_to_angle(identifier: str, coordinate: CoordinateEnum, value):
    if coordinate == CoordinateEnum.phi:
        await move_to_position(identifier, PositionCoordinates(phi=value))
    if coordinate == CoordinateEnum.zeta:
        await move_to_position(identifier, PositionCoordinates(zeta=value))
    if coordinate == CoordinateEnum.theta:
        await move_to_position(identifier, PositionCoordinates(theta=value))


async def move_to_angle_then_acquire_till_target(identifier: str, coordinate: CoordinateEnum, value):
    logging.info("moving then acquiring till target")
    print("moving then acquiring till target")
    await move_to_angle(identifier, coordinate, value)
    await comm.clear_and_arm_caen_acquisition(identifier, daemons.caen_charles_evans.url)
    await comm.clear_start_motrona_count(identifier, daemons.motrona_rbs.url)
    await comm.motrona_counting_done(daemons.motrona_rbs.url)


async def counting_pause_and_set_target(identifier: str, target):
    logging.info("pause counting and set target")
    print("pause counting and set target")
    await comm.pause_motrona_count(identifier + "_pause", daemons.motrona_rbs.url)
    await comm.set_motrona_target_charge(identifier + "_set_target_charge", daemons.motrona_rbs.url, target)


def make_coordinate_range(vary_coordinate: VaryCoordinate) -> List[float]:
    coordinate_range = np.arange(vary_coordinate.start, vary_coordinate.end + vary_coordinate.increment,
                                 vary_coordinate.increment)
    return np.around(coordinate_range, decimals=2)


async def get_packed_histogram(detector: CaenDetectorModel) -> List[int]:
    print("zzzz - waiting for some caen data")
    logging.info("zzz - waiting for some caen data")
    await asyncio.sleep(2)
    data = await comm.get_caen_histogram(daemons.caen_charles_evans.url, detector.board, detector.channel)
    packed = pack(data, detector.bins_min, detector.bins_max, detector.bins_width)
    return packed


def get_sum(data: List[int], window: Window):
    return sum(data[window.start:window.end])


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data


def try_copy(source, destination):
    logging.info("coppying {source} to {destination}".format(source=source, destination=destination))
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())


async def get_file_header(file_stem,  sample_id, detector_id, measuring_time_msec):
    aml_x_y_response = await comm.get_json_status(daemons.aml_x_y.url)
    aml_phi_zeta_response = await comm.get_json_status(daemons.aml_phi_zeta.url)
    aml_det_theta_response = await comm.get_json_status(daemons.aml_det_theta.url)
    motrona_response = await comm.get_json_status(daemons.motrona_rbs.url)
    header = """
 % Comments
 % Title                 := {title}
 % Section := <raw_data>
 *
 * Filename no extension := {filename}
 * DATE/Time             := {date}
 * MEASURING TIME[sec]   := {measure_time_sec}
 * ndpts                 := {ndpts}
 *
 * ANAL.IONS(Z)          := 4.002600
 * ANAL.IONS(symb)       := He+
 * ENERGY[MeV]           := 1.5 MeV
 * Charge[nC]            := {charge}
 *
 * Sample ID             := {sample_id}
 * Sample X              := {sample_x}
 * Sample Y              := {sample_y}
 * Sample Zeta           := {sample_zeta}
 * Sample Theta          := {sample_theta}
 * Sample Phi            := {sample_phi}
 * Sample Det            := {sample_det}
 *
 * Detector name         := {det_name}
 * Detector ZETA         := 0.0
 * Detector Omega[mSr]   := 0.42
 * Detector offset[keV]  := 33.14020
 * Detector gain[keV/ch] := 1.972060
 * Detector FWHM[keV]    := 18.0
 *
 % Section :=  </raw_data>
 % End comments
""".format(
        title=file_stem + "_" + detector_id,
        filename=file_stem,
        date=datetime.datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
        measure_time_sec=measuring_time_msec,
        ndpts=1024,
        charge=motrona_response["charge(nC)"],
        sample_id=sample_id,
        sample_x=aml_x_y_response["motor_1_position"],
        sample_y=aml_x_y_response["motor_2_position"],
        sample_phi=aml_phi_zeta_response["motor_1_position"],
        sample_zeta=aml_phi_zeta_response["motor_2_position"],
        sample_det=aml_det_theta_response["motor_1_position"],
        sample_theta=aml_det_theta_response["motor_2_position"],
        det_name=detector_id
    )
    return header


def format_caen_histogram(data: List[int]):
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += str(index) + ", " + str(energy_level) + "\n"
        index += 1
    return data_string


def store_yields(sub_folder, file_stem, angle_values, energy_yields):
    yields_file = file_stem + "_yields.txt"
    yields_path = output_dir.data / sub_folder / yields_file

    with open(yields_path, 'w+') as f:
        for index, angle in enumerate(angle_values):
            f.write("{angle}, {energy_yield}\n".format(angle=angle, energy_yield=energy_yields[index]))

    remote_yields_path = output_dir_remote.data / sub_folder / yields_file
    try_copy(yields_path, remote_yields_path)


async def store_histogram(sub_folder, file_stem, detector_id, measuring_time_msec, sample_id, data: List[int]):
    header = await get_file_header(file_stem, sample_id, detector_id, measuring_time_msec)
    formatted_data = format_caen_histogram(data)
    full_data = header + "\n" + formatted_data

    histogram_file = file_stem + "_" + detector_id + ".txt"
    histogram_path = output_dir.data / sub_folder / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    logging.info("Storing histogram data to path: " + str(histogram_path))
    with open(histogram_path, 'w+') as f:
        f.write(full_data)

    remote_histogram_path = output_dir_remote.data / sub_folder / histogram_file
    try_copy(histogram_path, remote_histogram_path)


def plot_energy_yields_and_clear(sub_folder, file_stem, angles, yields, smooth_angles, smooth_yields, angle_name):
    fig, ax = plt.subplots()
    ax.scatter(angles, yields, marker="+", color="red", label="Data Points")
    ax.axhline(np.amin(yields), label="Minimum", linestyle=":")
    ax.plot(smooth_angles, smooth_yields, color="green", label="Fit")
    ax.legend(loc=0)
    plt.xlabel(angle_name).set_fontsize(15)
    plt.ylabel("yield").set_fontsize(15)
    plt.title(file_stem)

    yield_plot_file = file_stem + ".png"
    yield_plot_path = output_dir.data / sub_folder / yield_plot_file
    Path.mkdir(yield_plot_path.parent, parents=True, exist_ok=True)
    logging.info("Storing yield plot to path: " + str(yield_plot_path))
    plt.savefig(yield_plot_path)
    plt.clf()

    remote_yield_plot_path = output_dir_remote.data / sub_folder / yield_plot_file
    try_copy(yield_plot_path, remote_yield_plot_path)


def append_histogram_plot(detector: CaenDetectorModel, data: List[int]):
    plt.plot(data, label=detector.identifier, color=detector.color)


def store_histogram_plot_and_clear(sub_folder, file_stem):
    histogram_file = file_stem + ".png"
    histogram_path = output_dir.data / sub_folder / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    logging.info("Storing histogram plot to path: " + str(histogram_path))
    plt.ylabel("yield")
    plt.xlabel("energy level")
    plt.grid()
    plt.legend()
    plt.savefig(histogram_path)
    remote_histogram_path = output_dir_remote.data / sub_folder / histogram_file
    try_copy(histogram_path, remote_histogram_path)
    plt.clf()


async def run_pre_channeling(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[CaenDetectorModel]):
    await move_to_position(recipe.title, recipe.start_position)
    angle_values = make_coordinate_range(recipe.vary_coordinate)
    angle_to_vary = recipe.vary_coordinate.name

    charge_limit_per_step = recipe.total_charge / len(angle_values)
    await counting_pause_and_set_target(recipe.title, charge_limit_per_step)
    detector_optimize = detectors[recipe.optimize_detector_index]
    active_detectors = [detectors[index] for index in recipe.detector_indices]

    energy_yields = []
    for angle in angle_values:
        start = time.time()
        await move_to_angle_then_acquire_till_target(recipe.title + "_" + str(angle), angle_to_vary, angle)
        data = await get_packed_histogram(detector_optimize)
        integrated_energy_yield = get_sum(data, recipe.integration_window)
        energy_yields.append(integrated_energy_yield)
        end = time.time()
        measuring_time_msec = end - start
        file_stem = recipe.file_stem + "_" + angle_to_vary + "_" + str(angle)

        for detector in active_detectors:
            data = await get_packed_histogram(detector)
            await store_histogram(sub_folder, file_stem, detector.identifier, measuring_time_msec, recipe.title, data)
            append_histogram_plot(detector, data)
        store_histogram_plot_and_clear(sub_folder, file_stem)

    store_yields(sub_folder, file_stem, angle_values, energy_yields)

    smooth_angles, smooth_yields = fit.fit_and_smooth(angle_values, energy_yields)
    plot_energy_yields_and_clear(sub_folder, file_stem, angle_values, energy_yields, smooth_angles, smooth_yields, angle_to_vary)
    index_for_minimum_yield = np.argmin(smooth_yields)
    min_angle = round(smooth_angles[index_for_minimum_yield], 2)

    await move_to_angle(recipe.title + "_move_to_min_angle", angle_to_vary, min_angle)


async def run_random(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[CaenDetectorModel]):
    start = time.time()
    await move_to_position(recipe.title, recipe.start_position)
    angle_values = make_coordinate_range(recipe.vary_coordinate)
    angle_to_vary = recipe.vary_coordinate.name

    charge_limit_per_step = recipe.total_charge / len(angle_values)
    await counting_pause_and_set_target(recipe.title, charge_limit_per_step)

    for angle in angle_values:
        await move_to_angle_then_acquire_till_target(recipe.title + "_" + str(angle), angle_to_vary, angle)
    end = time.time()
    measuring_time_msec = end - start

    active_detectors = [detectors[index] for index in recipe.detector_indices]
    for detector in active_detectors:
        data = await get_packed_histogram(detector)
        await store_histogram(sub_folder, recipe.file_stem, detector.identifier, measuring_time_msec, recipe.title, data)
        append_histogram_plot(detector, data)
    store_histogram_plot_and_clear(sub_folder, recipe.file_stem)


async def run_channeling(sub_folder, recipe: rbs.RbsRqmRecipe, detectors: List[CaenDetectorModel]):
    start = time.time()
    await move_to_position(recipe.title, recipe.start_position)
    await counting_pause_and_set_target(recipe.title, recipe.total_charge)
    end = time.time()
    measuring_time_msec = end - start

    active_detectors = [detectors[index] for index in recipe.detector_indices]
    for detector in active_detectors:
        data = await get_packed_histogram(detector)
        await store_histogram(sub_folder, recipe.file_stem, detector.identifier, measuring_time_msec, recipe.title, data)
        append_histogram_plot(detector, data)
    store_histogram_plot_and_clear(sub_folder, recipe.file_stem)


async def run_recipe_list(rbs_rqm: rbs.RbsRqm,  rbs_rqm_status: rbs.RbsRqmStatus):
    sub_folder = rbs_rqm.rqm_number

    rbs_rqm_status.run_status = rbs.StatusModel.Running
    rbs_rqm_status.recipe_list = rbs_rqm

    for recipe in rbs_rqm.recipes:
        if recipe.type == rbs.RecipeType.pre_channeling:
            await run_pre_channeling(sub_folder, recipe, rbs_rqm.detectors)
        if recipe.type == rbs.RecipeType.random:
            await run_random(sub_folder, recipe, rbs_rqm.detectors)
        if recipe.type == rbs.RecipeType.channeling:
            await run_channeling(sub_folder, recipe, rbs_rqm.detectors)

    rbs_rqm_status.run_status = rbs.StatusModel.Parking
    await move_to_position(rbs_rqm.rqm_number + "_parking" , rbs_rqm.parking_position)

    rbs_rqm_status.run_status = rbs.StatusModel.Idle
