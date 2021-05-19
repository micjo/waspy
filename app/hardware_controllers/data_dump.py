import logging
import requests
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from config import urls
from pathlib import Path
from app.rbs_experiment.entities import SceneModel,CaenDetectorModel
from typing import List

def store_and_plot_histograms(storage, scene: SceneModel, detectors: List[CaenDetectorModel]):
    print("store and plot histograms")
    for detector in detectors:
        b = str(detector.board)
        c = str(detector.channel)
        data = requests.get(urls.caen_charles_evans + "/histogram/" +b+ "-" +c).text.split(";")
        store_data(data, storage, scene, detector)

# def store_histogram_plot(data, storage, scene: SceneModel, title):
    # data_set0_y_values = []
    # data_set0_x_values = []
    # index = 0
    # for energylevel in data_set0.split(";"):
        # if (energylevel):
            # data_set0_x_values.append(index)
            # data_set0_y_values.append(int(energylevel))
            # index +=1

    # data_set1_y_values = []
    # data_set1_x_values = []
    # index = 0
    # for energylevel in data_set1.split(";"):
        # if (energylevel):
            # data_set1_x_values.append(index)
            # data_set1_y_values.append(int(energylevel))
            # index +=1

    # plot_location = storage / Path(scene.file + ".png")
    # fig = make_subplots(rows=2, cols=1, subplot_titles=("data_b6c0", "data_b6c1"))
    # fig.append_trace(go.Scatter( x = data_set0_x_values, y = data_set0_y_values, name="data_b6c0"), row=1, col=1) #type: ignore
    # fig.append_trace(go.Scatter( x = data_set1_x_values, y = data_set1_y_values, name="data_b6c1"), row=2, col=1) #type: ignore

    # fig.update_xaxes(title_text="Energy Bin", row=1, col=1) #type: ignore
    # fig.update_xaxes(title_text="Energy Bin", row=2, col=1) #type: ignore
    # fig.update_yaxes(title_text="Occurrence Rate", row=1, col=1) #type: ignore
    # fig.update_yaxes(title_text="Occurrence Rate", row=2, col=1) #type: ignore

    # fig.update_layout(height=1080, width=1920, title_text= scene.ftitle)
    # fig.write_image(plot_location.as_posix())


def store_data(data, storage, scene: SceneModel, detector: CaenDetectorModel):
    print("store_Data")
    aml_x_y_response = requests.get(urls.aml_x_y).json()
    aml_phi_zeta_response = requests.get(urls.aml_phi_zeta).json()
    aml_det_theta_response = requests.get(urls.aml_det_theta).json()
    motrona_response = requests.get(urls.motrona_rbs).json()

    b = str(detector.board)
    c = str(detector.channel)
    bc = "b"+b+"c"+c
    filename = storage / Path(scene.file  + "_" +bc+ ".txt")
    Path.mkdir(filename.parent, parents=True, exist_ok=True)
    header = get_file_header(scene, bc, aml_x_y_response, aml_phi_zeta_response, aml_det_theta_response, motrona_response)
    logging.info("storing histogram of " +bc)
    write_caen_histogram(filename, header, data)

def write_caen_histogram(location, header, dataDump):
    index = 0
    data = ""
    for energylevel in dataDump:
        if (energylevel):
            data += str(index) + ", "  + energylevel + "\n"
            index += 1

    with open(location, 'w+') as file:
        file.write(header)
        file.write(data)

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


