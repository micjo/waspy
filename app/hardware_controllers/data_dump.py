import logging
import math
import requests
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from config import daemons
from pathlib import Path
from app.rbs_experiment.entities import SceneModel,CaenDetectorModel
from typing import List

def store_and_plot_histograms(storage, scene: SceneModel, detectors: List[CaenDetectorModel]):
    print("store and plot histograms")

    fig = make_subplots(rows=len(detectors), cols=1)
    detector_index = 1
    for detector in detectors:
        packed_data = get_histogram_and_pack(detector)
        store_data(packed_data, storage, scene, detector)
        append_histogram_plot(packed_data, fig, detector, detector_index)
        detector_index += 1

    plot_location = storage / Path(scene.file + ".png")
    fig.update_layout(height=1080, width=1920, title_text= scene.ftitle)
    fig.write_image(plot_location.as_posix())

def get_histogram_and_pack(detector: CaenDetectorModel):
    b = str(detector.board)
    c = str(detector.channel)
    raw_data = requests.get(daemons.caen_charles_evans.url + "/histogram/" +b+ "-" +c).text.split(";")
    raw_data.pop()
    data = [int(x) for x in raw_data]
    return pack(data, detector.bins_min, detector.bins_max, detector.bins_width)

def append_histogram_plot(data: List[int], fig, detector: CaenDetectorModel, detector_index):
    x_values = list(range(0, len(data)))
    title = "b" + str(detector.board) + "c" + str(detector.channel)
    fig.append_trace(go.Scatter(x = x_values, y = data, name = title), row=detector_index, col=1) #type: ignore
    fig.update_xaxes(title_text="Energy Bin", row=detector_index, col=1) #type: ignore
    fig.update_yaxes(title_text="Occurrence Rate", row=detector_index, col=1) #type: ignore

def pack(data: List[int], channel_min, channel_max, channel_width) -> List[int]:
    subset = data[channel_min:channel_max]
    samples_to_group_in_bin = math.floor(len(subset) / channel_width)
    packed_data = []
    for index in range(0, samples_to_group_in_bin * channel_width, samples_to_group_in_bin):
        bin_sum = sum(subset[index:index + samples_to_group_in_bin])
        packed_data.append(bin_sum)
    return packed_data

def store_data(data: List[int], storage, scene: SceneModel, detector: CaenDetectorModel):
    aml_x_y_response = requests.get(daemons.aml_x_y.url).json()
    aml_phi_zeta_response = requests.get(daemons.aml_phi_zeta.url).json()
    aml_det_theta_response = requests.get(daemons.aml_det_theta.url).json()
    motrona_response = requests.get(daemons.motrona_rbs.url).json()

    b = str(detector.board)
    c = str(detector.channel)
    bc = "b"+b+"c"+c
    filename = storage / Path(scene.file  + "_" +bc+ ".txt")
    Path.mkdir(filename.parent, parents=True, exist_ok=True)
    header = get_file_header(scene, bc, aml_x_y_response, aml_phi_zeta_response, aml_det_theta_response, motrona_response)
    logging.info("storing histogram of " +bc)
    write_caen_histogram(filename, header, data)

def write_caen_histogram(location, header, data: List[int]):
    index = 0
    dataString = ""
    for energylevel in data:
        dataString += str(index) + ", "  + str(energylevel) + "\n"
        index += 1

    with open(location, 'w+') as file:
        file.write(header)
        file.write(dataString)

def get_file_header(scene: SceneModel, bc, aml_x_y_response, aml_phi_zeta_response, aml_det_theta_response, motrona_response):
    header = """
% Comments
% Title                 := {title}
% Section := <raw_data>
*
* Filename no extension := {filename}
* DATE/Time             := {date}
* MEASURING TIME[sec]   := {measure_time}
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
            title=scene.file + "_" +bc,
            filename=scene.file,
            date = datetime.datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
            measure_time = scene.measuring_time_msec,
            ndpts = 65535,
            charge = motrona_response["charge(nC)"],
            sample_id = scene.ftitle,
            sample_x = aml_x_y_response["motor_1_position"],
            sample_y = aml_x_y_response["motor_2_position"],
            sample_phi = aml_phi_zeta_response["motor_1_position"],
            sample_zeta = aml_phi_zeta_response["motor_2_position"],
            sample_det = aml_det_theta_response["motor_1_position"],
            sample_theta = aml_det_theta_response["motor_2_position"],
            det_name = bc
            )
    return header


