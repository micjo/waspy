import copy
from datetime import datetime
from typing import List

import numpy as np
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from waspy.iba.rbs_entities import RbsData, GraphGroup, AysFitResult, Graph
import matplotlib

matplotlib.use('Agg')


def plot_graph_group(graph_group: GraphGroup) -> Figure:
    nr_of_graphs = len(graph_group.graphs)
    fig, axs = plt.subplots(nr_of_graphs)
    fig.suptitle(graph_group.title)

    if nr_of_graphs == 1:
        axs = [axs]

    for (ax, graph) in zip(axs, graph_group.graphs):
        ax.set_title(graph.title)
        for plot in graph.plots:
            ax.plot(plot.points, label=plot.title)
        _configure_ax(ax, graph.x_label, graph.y_label)

    return fig


def plot_graph(graph: Graph) -> Figure:
    graph_group = GraphGroup(graphs=[graph])
    return plot_graph_group(graph_group)


def _configure_ax(ax, x_label, y_label):
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=":")
    ax.legend()
    ax.minorticks_on()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


def plot_energy_yields(title, fit_result: AysFitResult):
    fig, ax = plt.subplots()
    ax.scatter(fit_result.discrete_angles, fit_result.discrete_yields, marker="+", color="red", label="Data Points")
    ax.axhline(np.amin(fit_result.discrete_yields), label="Minimum", linestyle=":")
    smooth_angles = np.arange(fit_result.discrete_angles[1], fit_result.discrete_angles[-1], 0.01)
    smooth_yields = fit_result.fit_func(smooth_angles)
    ax.plot(smooth_angles, smooth_yields, color="green", label="Fit")
    ax.legend(loc=0)
    plt.xlabel("degrees").set_fontsize(15)
    plt.ylabel("yield").set_fontsize(15)
    plt.title(title)
    plt.grid()
    return fig


def serialize_yields(angle_values, energy_yields):
    content = ""
    for index, angle in enumerate(angle_values):
        content += "{angle}, {energy_yield}\n".format(angle=angle, energy_yield=energy_yields[index])
    return content


def serialize_histogram_header(rbs_data: RbsData, data_title: str, file_stem: str, sample_id: str, params: dict):
    now = datetime.utcnow().strftime("%Y.%m.%d__%H:%M__%S.%f")[:-3]

    header = f""" % Comments
 % Title                 := {file_stem + "_" + data_title}
 % Section := <raw_data>
 *
 * Filename no extension := {file_stem}
 * DATE/Time             := {now}
 * MEASURING TIME[sec]   := {rbs_data.measuring_time_msec}
 * ndpts                 := {1024}
 *
 * ANAL.IONS(Z)          := 4.002600
 * ANAL.IONS(symb)       := He+
 * ENERGY[MeV]           := {params.get("beam_energy_MeV", "")} MeV
 * Charge[nC]            := {rbs_data.accumulated_charge}
 *
 * Sample ID             := {sample_id}
 * Sample X              := {rbs_data.aml_x_y["motor_1_position"]}
 * Sample Y              := {rbs_data.aml_x_y["motor_2_position"]}
 * Sample Zeta           := {rbs_data.aml_phi_zeta["motor_1_position"]}
 * Sample Theta          := {rbs_data.aml_phi_zeta["motor_2_position"]}
 * Sample Phi            := {rbs_data.aml_det_theta["motor_1_position"]}
 * Sample Det            := {rbs_data.aml_det_theta["motor_2_position"]}
 *
 * Detector name         := {data_title}
 * Detector ZETA         := 0.0
 * Detector Omega[mSr]   := 0.42
 * Detector offset[keV]  := 33.14020
 * Detector gain[keV/ch] := 1.972060
 * Detector FWHM[keV]    := 18.0
 *
 % Section :=  </raw_data>
 % End comments"""
    return header



def format_caen_histogram(data: List[int]) -> str:
    index = 0
    data_string = ""
    for energy_level in data:
        data_string += f'{index}, {energy_level}\n'
        index += 1
    return data_string
