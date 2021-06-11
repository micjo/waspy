import app.rbs_experiment.fitting as fitter
import numpy as np

energy_yields = [451.0, 463.0, 424.0, 428.0, 451.0, 444.0, 449.0, 430.0, 451.0, 426.0, 387.0, 250.0, 148.0, 91.0, 136.0,
                 317.0, 374.0, 440.0, 396.0, 383.0, 388.0]

angles = ["-2.0", "-1.8", "-1.6", "-1.4", "-1.2", "-1.0", "-0.8", "-0.6", "-0.4", "-0.2", "-0.0", "0.2",
          "0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.6", "1.8", "2.0"]


def test_fit_and_smooth():
    float_angles = [float(x) for x in angles]
    smooth_angles, smooth_yields = fitter.fit_and_smooth(float_angles, energy_yields)
    min_angle = round(smooth_angles[np.argmin(smooth_yields)], 2)
    assert (min_angle == 0.57)
