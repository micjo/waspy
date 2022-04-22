from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from hive.hardware_control.rbs_entities import RbsHistogramGraphData, RbsHistogramGraphDataSet


def plot_rbs_histograms(histogram_data: RbsHistogramGraphData) -> Figure:

    nr_of_histograms = len(histogram_data.histograms)
    fig, axs = plt.subplots(nr_of_histograms)
    fig.suptitle(histogram_data.graph_title)

    if nr_of_histograms == 1:
        axs = [axs]

    for histogram, ax in zip(histogram_data.histograms, axs):
        ax.plot(histogram.data, label=histogram.title)
        _configure_ax(ax, histogram_data.x_label, histogram_data.y_label)
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
