import logging
from typing import List

import numpy as np
from scipy import optimize
from scipy.optimize import Bounds, fmin, fminbound


def get_angle_for_minimum_yield(smooth_angles, smooth_yields) -> float:
    smooth_angle_for_minimum_yield = round(smooth_angles[np.argmin(smooth_yields)], 2)
    log_line = "[WASPY.IBA.RBS_YIELD_ANGLE_FIT] Minimum yield found at: [angle: yield] = [{angle}: {energy_yield}]" \
        .format(angle=smooth_angle_for_minimum_yield, energy_yield=round(np.amin(smooth_yields), 2))
    logging.info(log_line)
    return smooth_angle_for_minimum_yield


def constant_func(x, constant):
    # Simply returning the constant makes np arange return a single value, We want a list of the same value
    return [constant for _ in range(len(x))]


def fit_and_smooth(angles, yields, algorithm_type=0):
    """Will fit a curve using x and y. When the fit is found, recalculate the y values with a more finely
    distributed x (smooth) (interpolated)."""

    # Tried to use scipy minimize, fminbound here - but it doesnt work as expected in all cases
    # Just eval the entire range and get the minimum - will get very slow with large arrays
    if algorithm_type == 0:
        try:
            return attempt_lower_fit(angles, yields)
        except:
            minimum = min(yields)
            def fit_func(x):
                return constant_func(x, minimum)
            return fit_func, angles[yields.index(minimum)]

    else:
        return attempt_fit(angles, yields)


def attempt_fit(angles, yields):
    p_start = np.amax(yields)
    r_start = angles[np.argmin(yields)]

    arg_bounds = (
        (-np.inf, 0, -np.inf, -np.inf, 0, -np.inf), (np.inf, np.inf, np.inf, np.inf, np.inf, np.inf))
    [p, q, r, s, t, u], covariance = optimize.curve_fit(fit, angles, yields,
                                                        p0=[p_start, 100.0, r_start, 0.3, 50, -1.0],
                                                        bounds=arg_bounds)

    def fit_func(x):
        return fit(x, p, q, r, s, t, u)
    smooth_x = [x for x in np.arange(angles[0], angles[-1], 0.01)]
    smooth_y = [fit(x, p, q, r, s, t, u) for x in smooth_x]
    min_x = round(smooth_x[np.argmin(smooth_y)], 2)
    return fit_func, min_x


def fit(x, p, q, r, s, t, u):
    value = p + t * np.exp(-np.power(x - r, 2) / (2 * np.power(4 * s, 2))) - q * np.exp(
        -np.power(x - r, 2) / (2 * np.power(s, 2))) + u * x
    return value


def attempt_lower_fit(angles, yields):
    p_start = np.amax(yields)
    r_start = angles[np.argmin(yields)]
    # [p, q, r, s, t, u], covariance = optimize.curve_fit(lower_order_fit, angles, yields,
    #                                                     p0=[p_start, 100.0, r_start, 0.3, -1.0, -1.0])
    [p, q, r, s, t, u], covariance = optimize.curve_fit(lower_order_fit, angles, yields,
                                                        p0=[p_start, 100.0, r_start, 0.3, -1.0, -1.0])

    def fit_func(x):
        return lower_order_fit(x, p, q, r, s, t, u)

    smooth_x = [x for x in np.arange(angles[0], angles[-1], 0.01)]
    smooth_y = [fit(x, p, q, r, s, t, u) for x in smooth_x]
    min_x = round(smooth_x[np.argmin(smooth_y)], 2)
    return fit_func, min_x


def lower_order_fit(x, p, q, r, s, t, u):
    return p - q * np.exp(-np.power(x - r, 2) / (2 * np.power(s, 2))) + t * np.power(x, 2) + u * x
