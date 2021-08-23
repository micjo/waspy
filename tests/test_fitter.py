import app.rbs_experiment.yield_angle_fit as fitter
import pytest

energy_yields = [451.0, 463.0, 424.0, 428.0, 451.0, 444.0, 449.0, 430.0, 451.0, 426.0, 387.0, 250.0, 148.0, 91.0, 136.0,
                 317.0, 374.0, 440.0, 396.0, 383.0, 388.0]

angles = ["-2.0", "-1.8", "-1.6", "-1.4", "-1.2", "-1.0", "-0.8", "-0.6", "-0.4", "-0.2", "-0.0", "0.2",
          "0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0"]

energy_yields = [451.0, 463.0, 424.0, 428.0, 451.0, 444.0, 449.0, 430.0, 451.0, 426.0, 387.0, 250.0, 148.0, 91.0, 136.0,
                 317.0, 374.0, 440.0, 396.0, 383.0, 388.0]

energy_yields_test = [434, 451, 385, 367, 400, 458, 526, 516, 286, 202, 260, 457, 508, 482, 424, 399, 361, 377, 400,
                      444, 412]

sample_data_01 = [2443.0, 2497.0, 2547.0, 2614.0, 2597.0, 2680.0, 1966.0, 725.0, 1001.0, 2269.0, 2393.0, 2272.0, 2226.0,
                  2215.0, 2208.0, 2196.0, 2025.0, 2246.0, 2486.0, 2524.0, 2551.0]
sample_data_01_expect = -0.53


def test_fit_and_smooth():
    from unittest.mock import patch, mock_open
    patch("builtins.open", mock_open(read_data="data"))

    import app.rbs_experiment.yield_plot as plotting

    float_angles = [float(x) for x in angles]
    data_index = 0
    with open("sample_data_01.txt", "r") as f:
        for line in f:
            data_set = line.split("->")
            expected_value = float(data_set[1])
            yields = [float(x) for x in data_set[0].split(" ") if x]
            smooth_angles, smooth_yields = fitter.fit_and_smooth(float_angles, yields, 0)
            assert (fitter.get_angle_for_minimum_yield(smooth_angles, smooth_yields)) == pytest.approx(expected_value)
            plotting.plot_energy_yields("plots",  str(data_index), float_angles, yields, smooth_angles, smooth_yields)
            data_index += 1
