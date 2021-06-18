import app.rbs_experiment.plotting as plot


def test_plot():
    plot.plot_histograms_and_clear("eee", "file_stem", "identifier", [[0,1,2], [0,5,6]])