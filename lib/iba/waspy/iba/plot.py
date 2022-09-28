from datetime import datetime
from typing import List

import numpy as np
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from waspy.iba.rbs_entities import RbsHistogramGraphData, RbsData, RbsHistogramGraphDataSet, Graph, GraphGroup


def plot_graph(graph: Graph) -> Figure:
    nr_of_plots = len(graph.plots)
    fig, axs = plt.subplots(nr_of_plots)
    fig.suptitle(graph.title)

    if nr_of_plots == 1:
        axs = [axs]

    for plot, ax in zip(graph.plots, axs):
        ax.plot(plot.points, label=plot.title)
        _configure_ax(ax, graph.x_label, graph.y_label)
    return fig


def plot_graph_group(graph_group: GraphGroup) -> Figure:
    nr_of_graphs = len(graph_group.graphs)
    fig, axs = plt.subplots(nr_of_graphs)
    fig.suptitle(graph_group.title)

    for (ax, graph) in zip(axs, graph_group.graphs):
        ax.set_title(graph.title)
        for plot in graph.plots:
            ax.plot(plot.points, label=plot.title)
        _configure_ax(ax, graph.x_label, graph.y_label.y_label)

    return fig



def plot_compare_rbs_histograms(histogram_dataset: RbsHistogramGraphDataSet):
    nr_of_histograms = len(histogram_dataset.histograms)
    fig, axs = plt.subplots(nr_of_histograms)
    fig.suptitle(histogram_dataset.graph_title)

    for (ax, histogram_compare) in zip(axs, histogram_dataset.histograms):
        for histogram in histogram_compare:
            ax.plot(histogram.data, label=histogram.title)
            _configure_ax(ax, histogram_dataset.x_label, histogram_dataset.y_label)

    return fig


def _configure_ax(ax, x_label, y_label):
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=":")
    ax.legend()
    ax.minorticks_on()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


# def plot_histograms(rbs_data: RbsData, file_stem: str):
#     rbs_histogram_graph_data = RbsHistogramGraphData(graph_title=file_stem, histograms=rbs_data.histograms)
#     fig = plot_rbs_histograms(rbs_histogram_graph_data)
#     return fig
#
#
# def plot_compare(fixed_data: List[HistogramData], random_data: List[HistogramData], file_stem):
#     histograms = []
#
#     for (random, fixed) in zip(random_data, fixed_data):
#         random.title += "_random"
#         fixed.title += "_fixed"
#         histograms.append([random, fixed])
#
#     rbs_histogram_graph_data_set = RbsHistogramGraphDataSet(graph_title=file_stem,
#                                                             histograms=histograms,
#                                                             x_label="energy level",
#                                                             y_label="yield")
#
#     fig = plot_compare_rbs_histograms(rbs_histogram_graph_data_set)
#     return fig
#

def plot_energy_yields(title,
                       angles: List[float], yields: List[int], smooth_angles: List[float],
                       smooth_yields: List[float]):
    fig, ax = plt.subplots()
    ax.scatter(angles, yields, marker="+", color="red", label="Data Points")
    ax.axhline(np.amin(yields), label="Minimum", linestyle=":")
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
 * ENERGY[MeV]           := {params.get("beam_energy_MeV","")} MeV
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
