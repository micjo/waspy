import logging
import numpy as np
import scipy.optimize as opt


def get_angle_for_minimum_yield(smooth_angles, smooth_yields) -> float:
    smooth_angle_for_minimum_yield = round(smooth_angles[np.argmin(smooth_yields)], 2)
    log_line = "Minimum yield found at: [angle: yield] = [{angle}: {energy_yield}]" \
        .format(angle=smooth_angle_for_minimum_yield, energy_yield=round(np.amin(smooth_yields), 2))
    logging.info(log_line)
    return smooth_angle_for_minimum_yield


def fit_and_smooth(angles, yields, algorithm_type=0):
    """Will fit a curve using x and y. When the fit is found, recalculate the y values with a more finely
    distributed x (smooth) (interpolated). Then the minimum y is found and the corresponding x value i returned"""
    if algorithm_type == 0:
        return attempt_lower_fit(angles, yields)
    else:
        return attempt_fit(angles, yields)


def attempt_fit(angles, yields):
    p_start = np.amax(yields)
    r_start = angles[np.argmin(yields)]

    arg_bounds = (
        (-np.inf, 0, -np.inf, -np.inf, 0, -np.inf), (np.inf, np.inf, np.inf, np.inf, np.inf, np.inf))
    [p, q, r, s, t, u], covariance = opt.curve_fit(fit, angles, yields, p0=[p_start, 100.0, r_start, 0.3, 50, -1.0],
                                                   bounds=arg_bounds)

    smooth_angles = [x for x in np.arange(angles[0], angles[-1], 0.001)]
    smooth_yields = [fit(x, p, q, r, s, t, u) for x in smooth_angles]

    return smooth_angles, smooth_yields


def fit(x, p, q, r, s, t, u):
    return p + t * np.exp(-np.power(x - r, 2) / (2 * np.power(4 * s, 2))) - q * np.exp(
        -np.power(x - r, 2) / (2 * np.power(s, 2))) + u * x


def attempt_lower_fit(angles, yields):
    p_start = np.amax(yields)
    r_start = angles[np.argmin(yields)]

    [p, q, r, s, t, u], covariance = opt.curve_fit(lower_order_fit, angles, yields, p0=[p_start, 100.0, r_start, 0.3, -1.0, -1.0])
    smooth_angles = [x for x in np.arange(angles[0], angles[-1], 0.001)]
    smooth_yields = [lower_order_fit(x, p, q, r, s, t, u) for x in smooth_angles]
    return smooth_angles, smooth_yields


def lower_order_fit(x, p, q, r, s, t, u):
    return p - q * np.exp(-np.power(x - r, 2) / (2 * np.power(s, 2))) + t * np.power(x, 2) + u * x


