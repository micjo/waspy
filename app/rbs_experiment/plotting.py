import logging
from pathlib import Path
from typing import List
import numpy as np
from matplotlib import pyplot as plt

import app.rbs_experiment.entities as rbs
from app.rbs_experiment.storing import try_copy
from app.setup.config import output_dir, output_dir_remote


def plot_energy_yields(sub_folder, file_stem, angles, yields, smooth_angles, smooth_yields):
    fig, ax = plt.subplots()
    ax.scatter(angles, yields, marker="+", color="red", label="Data Points")
    ax.axhline(np.amin(yields), label="Minimum", linestyle=":")
    ax.plot(smooth_angles, smooth_yields, color="green", label="Fit")
    ax.legend(loc=0)
    plt.xlabel("degrees").set_fontsize(15)
    plt.ylabel("yield").set_fontsize(15)
    plt.title(file_stem)
    plt.grid()

    yield_plot_file = file_stem + "_yields.png"
    yield_plot_path = output_dir.data / sub_folder / yield_plot_file
    Path.mkdir(yield_plot_path.parent, parents=True, exist_ok=True)
    logging.info("Storing yield plot to path: " + str(yield_plot_path))
    plt.savefig(yield_plot_path)
    plt.clf()

    remote_yield_plot_path = output_dir_remote.data / sub_folder / yield_plot_file
    try_copy(yield_plot_path, remote_yield_plot_path)


def set_plot_title(title: str):
    plt.title(title)


def plot_histograms_and_clear(sub_folder, file_stem, detectors: List[rbs.CaenDetectorModel], data:List[List[int]]):

    fig, axs = plt.subplots(len(data))
    fig.suptitle(file_stem)

    for index, ax in enumerate(axs):
        ax.plot(data[index], label=detectors[index].identifier)
        ax.grid(which='major')
        ax.grid(which='minor', linestyle=":")
        ax.minorticks_on()
        ax.legend()
        ax.set_xlabel("energy level")
        ax.set_ylabel("yield")

    plt.subplots_adjust(hspace=0.5)

    histogram_file = file_stem + ".png"
    histogram_path = output_dir.data / sub_folder / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    logging.info("Storing histogram plot to path: " + str(histogram_path))
    plt.savefig(histogram_path)
    remote_histogram_path = output_dir_remote.data / sub_folder / histogram_file
    try_copy(histogram_path, remote_histogram_path)
    plt.close(fig)