import comm
import logging
import os
import errno
import requests
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_histograms(data_set0, data_set1, storage, scene):
    data_set0_y_values = []
    data_set0_x_values = []
    index = 0
    for energylevel in data_set0.split(";"):
        if (energylevel):
            data_set0_x_values.append(index)
            data_set0_y_values.append(int(energylevel))
            index +=1

    data_set1_y_values = []
    data_set1_x_values = []
    index = 0
    for energylevel in data_set1.split(";"):
        if (energylevel):
            data_set1_x_values.append(index)
            data_set1_y_values.append(int(energylevel))
            index +=1

    plot_location = storage + "/" + scene["file"] + ".png"
    fig = make_subplots(rows=2, cols=1, subplot_titles=("data_b6c0", "data_b6c1"))
    fig.append_trace(go.Scatter( x = data_set0_x_values, y = data_set0_y_values, name="data_b6c0"), row=1, col=1)
    fig.append_trace(go.Scatter( x = data_set1_x_values, y = data_set1_y_values, name="data_b6c1"), row=2, col=1)

    fig.update_xaxes(title_text="Energy Bin", row=1, col=1)
    fig.update_xaxes(title_text="Energy Bin", row=2, col=1)
    fig.update_yaxes(title_text="Occurrence Rate", row=1, col=1)
    fig.update_yaxes(title_text="Occurrence Rate", row=2, col=1)

    fig.update_layout(height=1080, width=1920, title_text= scene["ftitle"])
    fig.write_image(plot_location)

def store_and_plot_histograms(config, storage, scene):
    data_set0 = store_histogram(config,storage,scene,6,0)
    data_set1 = store_histogram(config,storage,scene,6,1)
    plot_histograms(data_set0, data_set1, storage, scene)


def store_histogram(config, storage, scene, board, channel):
    aml_x_y_response = comm.get_json_status(config["aml_x_y"])
    aml_phi_zeta_response = comm.get_json_status(config["aml_phi_zeta"])
    aml_det_theta_response = comm.get_json_status(config["aml_det_theta"])
    motrona_response = comm.get_json_status(config["motrona_rbs"])

    b = str(board)
    c = str(channel)
    bc = "b"+b+"c"+c
    filename = storage + "/" + scene["file"]  + "_" +bc+ ".txt"
    print(filename)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    header = get_file_header(scene, bc, aml_x_y_response, aml_phi_zeta_response, aml_det_theta_response, motrona_response)
    logging.info("storing histogram of " +bc)
    caen_histogram = requests.get(config["caen_charles_evans"] + "/histogram/" +b+ "-" +c)
    write_caen_histogram(filename, header, caen_histogram.text)

    return caen_histogram.text


def get_file_header(scene, bc, aml_x_y_response, aml_phi_zeta_response, aml_det_theta_response, motrona_response):
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
            title=scene["file"]+ "_" +bc,
            filename=scene["file"],
            date = datetime.datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3],
            measure_time = scene["measuring_time(sec)"],
            ndpts = 65535,
            charge = motrona_response["charge(nC)"],
            sample_id = scene["ftitle"],
            sample_x = aml_x_y_response["motor_1_position"],
            sample_y = aml_x_y_response["motor_2_position"],
            sample_phi = aml_phi_zeta_response["motor_1_position"],
            sample_zeta = aml_phi_zeta_response["motor_2_position"],
            sample_det = aml_det_theta_response["motor_1_position"],
            sample_theta = aml_det_theta_response["motor_2_position"],
            det_name = bc
            )
    return header


def write_caen_histogram(location, header, dataDump):
    index = 0
    data = ""
    for energylevel in dataDump.split(";"):
        if (energylevel):
            data += str(index) + ", "  + energylevel + "\n"
            index += 1

    with open(location, 'w+') as file:
        file.write(header)
        file.write(data)
