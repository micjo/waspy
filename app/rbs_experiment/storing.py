import datetime
import logging
import traceback
from pathlib import Path
from shutil import copy2
from typing import List

from app.hardware_controllers import daemon_comm as comm
from app.setup.config import daemons, output_dir, output_dir_remote


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
    header = """ % Comments
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
 % End comments""".format(
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