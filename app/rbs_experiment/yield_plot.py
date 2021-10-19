import logging
from pathlib import Path
from typing import List
import numpy as np
from matplotlib import pyplot as plt

import app.rbs_experiment.entities as rbs
from app.rbs_experiment.yield_store import try_copy
from app.setup.config import cfg


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
    yield_plot_path = cfg.output_dir.data / sub_folder / yield_plot_file
    Path.mkdir(yield_plot_path.parent, parents=True, exist_ok=True)
    logging.info("Storing yield plot to path: " + str(yield_plot_path))
    plt.savefig(yield_plot_path)
    plt.clf()

    remote_yield_plot_path = cfg.output_dir_remote.data / sub_folder / yield_plot_file
    try_copy(yield_plot_path, remote_yield_plot_path)
    plt.close(fig)


def set_plot_title(title: str):
    plt.title(title)


def plot_compare(settings: rbs.RbsRqmSettings, file_stem, fixed_data: List[List[int]], random_data: List[List[int]]):
    nr_of_histograms = len(fixed_data)

    fixed_labels = [detector.identifier + "_fixed" for detector in settings.detectors]
    random_labels = [detector.identifier + "_random" for detector in settings.detectors]

    fig, axs = plt.subplots(nr_of_histograms)

    for index, ax in enumerate(axs):
        ax.plot(fixed_data[index], label=fixed_labels[index])
        ax.plot(random_data[index], label=random_labels[index])
        ax.grid(which='major')
        ax.grid(which='minor', linestyle=":")
        ax.minorticks_on()
        ax.legend()
        ax.set_xlabel("energy level")
        ax.set_ylabel("yield")

    plt.subplots_adjust(hspace=0.5)

    histogram_file = file_stem + ".png"
    histogram_path = cfg.output_dir.data / settings.get_folder() / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    logging.info("Storing histogram plot to path: " + str(histogram_path))
    plt.savefig(histogram_path)
    remote_histogram_path = cfg.output_dir_remote.data / settings.get_folder() / histogram_file
    try_copy(histogram_path, remote_histogram_path)
    plt.close(fig)


def plot_histograms_and_clear(settings: rbs.RbsRqmSettings, file_stem, data: List[List[int]]):
    fig, axs = plt.subplots(len(data))
    fig.suptitle(file_stem)

    for index, ax in enumerate(axs):
        ax.plot(data[index], label=settings.detectors[index].identifier)
        ax.grid(which='major')
        ax.grid(which='minor', linestyle=":")
        ax.minorticks_on()
        ax.legend()
        ax.set_xlabel("energy level")
        ax.set_ylabel("yield")

    plt.subplots_adjust(hspace=0.5)

    histogram_file = file_stem + ".png"
    histogram_path = cfg.output_dir.data / settings.rqm_number / histogram_file
    Path.mkdir(histogram_path.parent, parents=True, exist_ok=True)
    logging.info("Storing histogram plot to path: " + str(histogram_path))
    plt.savefig(histogram_path)
    remote_histogram_path = cfg.output_dir_remote.data / settings.rqm_number / histogram_file
    try_copy(histogram_path, remote_histogram_path)
    plt.close(fig)
