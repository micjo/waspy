import logging
import math
import requests
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from app.config.config import daemons, output_dir, output_dir_remote
from pathlib import Path
from app.rbs_experiment.entities import Recipe, CaenDetectorModel
from typing import List
from shutil import copy2
import traceback

def _try_copy(source, destination):
    try:
        Path.mkdir(destination.parent, exist_ok=True)
        copy2(source, destination)
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())


def store_histogram_and_append_to_plot(rqm_number, recipe: Recipe, detector: CaenDetectorModel, fig, detector_index):
    header = get_file_header(recipe, detector)
    packed_data = get_histogram_and_pack(detector)
    formatted_data = format_caen_histogram(packed_data)
    full_data = header + "\n" + formatted_data

    histogram_file = recipe.file + "_b" + str(detector.board) + "c" + str(detector.channel) + ".txt"
    histogram_path = output_dir.data / rqm_number / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    with open(histogram_path, 'w+') as f: f.write(full_data)

    remote_histogram_path = output_dir_remote.data / rqm_number / histogram_file
    _try_copy(histogram_path, remote_histogram_path)

    append_histogram_plot(packed_data, fig, detector, detector_index)


def store_and_plot_histograms(rqm_number, recipe: Recipe, detectors: List[CaenDetectorModel]):
    fig = make_subplots(rows=len(detectors), cols=1)
    fig.update_layout(height=1080, width=1920, title_text=recipe.ftitle)
    detector_index = 1

    for detector in detectors:
        store_histogram_and_append_to_plot(rqm_number, recipe, detector, fig, detector_index)
        detector_index += 1

    plot_file = recipe.file + ".png"
    plot_location = output_dir.data / rqm_number / plot_file
    fig.write_image(plot_location.as_posix())

    remote_plot_location = output_dir_remote.data / rqm_number / plot_file
    _try_copy(plot_location, remote_plot_location)


def get_histogram_and_pack(detector: CaenDetectorModel):
    b = str(detector.board)
    c = str(detector.channel)
    raw_data = requests.get(daemons.caen_charles_evans.url + "/histogram/" + b + "-" + c).text.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return pack(data, detector.bins_min, detector.bins_max, detector.bins_width)


def append_histogram_plot(data: List[int], fig, detector: CaenDetectorModel, detector_index):
    x_values = list(range(0, len(data)))
    title = "b" + str(detector.board) + "c" + str(detector.channel)
    fig.append_trace(go.Scatter(x=x_values, y=data, name=title), row=detector_index, col=1)  # type: ignore
    fig.update_xaxes(title_text="Energy Bin", row=detector_index, col=1)  # type: ignore
    fig.update_yaxes(title_text="Occurrence Rate", row=detector_index, col=1)  # type: ignore


def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data


def format_caen_histogram(data: List[int]):
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += " " + str(index) + ", " + str(energy_level) + "\n"
        index += 1
    return data_string


def get_file_header(scene: Recipe, detector: CaenDetectorModel):
    bc = str(detector.board) + str(detector.channel)
    aml_x_y_response = requests.get(daemons.aml_x_y.url).json()
    aml_phi_zeta_response = requests.get(daemons.aml_phi_zeta.url).json()
    aml_det_theta_response = requests.get(daemons.aml_det_theta.url).json()
    motrona_response = requests.get(daemons.motrona_rbs.url).json()
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
        title=scene.file + "_" + bc,
        filename=scene.file,
        date=datetime.datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
        measure_time_sec=scene.measuring_time_sec,
        ndpts=1024,
        charge=motrona_response["charge(nC)"],
        sample_id=scene.ftitle,
        sample_x=aml_x_y_response["motor_1_position"],
        sample_y=aml_x_y_response["motor_2_position"],
        sample_phi=aml_phi_zeta_response["motor_1_position"],
        sample_zeta=aml_phi_zeta_response["motor_2_position"],
        sample_det=aml_det_theta_response["motor_1_position"],
        sample_theta=aml_det_theta_response["motor_2_position"],
        det_name=bc
    )
    return header
