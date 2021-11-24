# -*- coding: utf-8 -*-

import math

from numpy import arange


def factorial(n: int):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def bezier_curve(points: list, t: float):
    n = len(points) - 1
    x = ((1 - t) ** n) * points[0][0]
    y = ((1 - t) ** n) * points[0][1]

    for i in range(1, n):
        binomial = factorial(n) / (factorial(i) * factorial(n - i))
        polynomial = binomial * (t ** i) * ((1 - t) ** (n - i))
        x += polynomial * points[i][0]
        y += polynomial * points[i][1]
    x += (t ** n) * points[n][0]
    y += (t ** n) * points[n][1]

    return x, y


def bezier_coefficient(lst: list):
    c = []
    n = len(lst) - 1
    for j in range(0, n + 1):
        cx, cy = 0, 0
        binom = factorial(n) / factorial(n - j)
        for i in range(j + 1):
            polynom = ((-1) ** (i + j)) / (factorial(i) * factorial(j - i))
            cx += binom * polynom * lst[i][0]
            cy += binom * polynom * lst[i][1]
            # print(j, i, cx, cy)
        c.append((cx, cy))
    return c


def bezier_curve_intersect(x, coefficients):

    xleft = get_polynomial_bezier_curve_point(0.0, coefficients)
    xright = get_polynomial_bezier_curve_point(1.0, coefficients)

    if x < xleft or x > xright:
        return False
    else:
        return True


def get_bezier_curve_parameter(x, coefficients, start=0.0, stop=1.0, eps=10**-6):

    xleft = get_polynomial_bezier_curve_point(0.0, coefficients)
    xright = get_polynomial_bezier_curve_point(1.0, coefficients)

    step = (stop - start) / 1000
    t = arange(start, stop, step)
    xmid = get_polynomial_bezier_curve_point(t[int(len(t) / 2)], coefficients)

    if abs(xleft - x) <= eps:
        return 0.0
    elif abs(xright - x) <= eps:
        return 1.0
    elif abs(xmid - x) <= eps:
        return t[int(len(t) / 2)]
    else:
        start = t[0] if xmid > x else t[int(len(t) / 2)]
        stop = t[int(len(t) / 2)] if xmid > x else t[len(t) - 1]
        return get_bezier_curve_parameter(x, coefficients, start, stop)


def get_polynomial_bezier_curve_point(t, coefficients):
    n = len(coefficients) - 1
    x = coefficients[0]

    for i in range(1, n+1):
        x += coefficients[i] * t ** i

    return x


def get_bezier_curve_derivative(control_points: list, t: float):

    n = len(control_points) - 1
    if n <= 1:
        return 0
    else:
        x = ((1 - t) ** (n - 1)) * (control_points[1][0] - control_points[0][0])
        y = ((1 - t) ** (n - 1)) * (control_points[1][1] - control_points[0][1])

        for i in range(1, n):
            binomial = factorial(n - 1) / factorial(i) * factorial(n - 1 - i)
            polynomial = binomial * (t ** i) * ((1 - t) ** (n - 1 - i))
            x += polynomial * (control_points[i + 1][0] - control_points[i][0])
            y += polynomial * (control_points[i + 1][1] - control_points[i][1])

        return n * x, n * y


# This function doesn't work properly. Curvature has to be determined to define properly shifting
# def find_intersection(x: float, y: float, slope: float, coefficients, start=0.0, stop=1.0, eps=10**-6):
#
#     step = (stop - start) / 1000
#     t = arange(start, stop, step)
#     x_bezier = get_polynomial_bezier_curve_point(t[int(len(t) / 2)], coefficients[0])
#     y_bezier = get_polynomial_bezier_curve_point(t[int(len(t) / 2)], coefficients[1])
#     y_line = y + (x_bezier - x) * math.tan(math.radians(slope))
#
#     if abs(y_bezier - y_line) < eps:
#         return x_bezier, y_bezier
#     else:
#         start = t[0] if y_bezier > y_line else t[int(len(t) / 2)]
#         stop = t[int(len(t) / 2)] if y_bezier > y_line else t[len(t) - 1]
#         return find_intersection(x, y, slope, coefficients, start, stop)


def get_partial_length(x: list, y: list, z: list, t: float):

    return t * (sum(x) ** 2 + sum(y) ** 2 + sum(z) ** 2) ** 0.5


def polynomial_function_derivative(coefficients: list, x: float):

    return sum(c * x ** i for i, c in enumerate(coefficients))


def get_coordinate_partial_length(x: list, y: list, t: float):

    slope = math.tan((y[0] - sum(y[1:])) / (x[0] - sum(x[1:])))
    return (
        x[0] + t * get_partial_length(x, y, [], t) * math.cos(slope),
        y[0] + t * get_partial_length(x, y, [], t) * math.sin(slope)
    )


def circle(x0: float = 0, y0: float = 0, r: float = 1,
           phi_1: float = 0, phi_2: float = 360, **kwargs):

    n = kwargs.get('n', 10)
    reverse = kwargs.get('reverse', 1)
    phi_1 = math.radians(phi_1)
    phi_2 = math.radians(phi_2)
    dphi = (phi_2 - phi_1) / n
    xy = []

    for i in list(range(0, n + 1)):
        xy.append((
            x0 + r * math.cos(phi_1 + i * dphi * reverse),
            y0 + r * math.sin(phi_1 + i * dphi * reverse)
        ))

    return xy


def line_intersection(xy_slope: list):

    x1, x2 = xy_slope[0][0], xy_slope[1][0]
    y1, y2 = xy_slope[0][1], xy_slope[1][1]
    slope1, slope2 = math.radians(xy_slope[0][2]), math.radians(xy_slope[1][2])
    if slope1 == slope2:
        return ()

    xp = y1 - y2 + x2 * math.tan(slope2) - x1 * math.tan(slope1)
    xp /= (math.tan(slope2) - math.tan(slope1))
    yp = y1 + math.tan(slope1) * (xp - x1)

    return xp, yp


def coordinate_system_rotation(x, y, angle):

    r = (x ** 2 + y ** 2) ** 0.5
    d_fi = math.radians(angle)
    fi = math.tan(y / x)
    return r * math.cos(fi + d_fi), r * math.sin(fi + d_fi)


def get_slope(x, y):
    return math.degrees(math.tan((y[0] - sum(y[1:]) / (x[0] - sum(x[1:])))))
