import app.rbs_experiment.py_fitter as fitter
import numpy as np

energy_yields = [451.0, 463.0, 424.0, 428.0, 451.0, 444.0, 449.0, 430.0, 451.0, 426.0, 387.0, 250.0, 148.0, 91.0, 136.0,
                 317.0, 374.0, 440.0, 396.0, 383.0, 388.0]

angles = ["-2.0", "-1.8", "-1.6", "-1.4", "-1.2", "-1.0", "-0.8", "-0.6", "-0.4", "-0.2", "-0.0", "0.2",
          "0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0"]


# def test_fit_and_plot_from_file():
#     min_index, min, min_data = fitter.fit_and_plot("testing","some_axis")
#     assert(min == 79.5)
#     assert(min_data == 91.0)
#     assert(min_index == 0.57)


def test_fit_and_plot():
    float_angles = [float(x) for x in angles]
    minimum_angle = fitter.fit_smooth_and_minimize(float_angles, energy_yields, save_plot=True, plot_file_name="plot.png", plot_x_label="test")
    assert (minimum_angle == 0.57)
