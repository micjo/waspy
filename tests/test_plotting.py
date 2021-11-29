import app.rbs.yield_plot as plot


def test_plot():
    plot.plot_histograms("eee", "file_stem", "identifier", [[0, 1, 2], [0, 5, 6]])