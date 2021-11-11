# -*- coding: utf-8 -*-

import math
import os

from common_class import CommonClass


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
    for j in range(0, n+1):
        cx, cy = 0, 0
        binom = factorial(n) / factorial(n - j)
        for i in range(j + 1):
            polynom = ((-1) ** (i + j)) / (factorial(i) * factorial(j - i))
            cx += binom * polynom * lst[i][0]
            cy += binom * polynom * lst[i][1]
            # print(j, i, cx, cy)
        c.append((cx, cy))
    return c


# def curve_length(coefficients: list, intervals: list):
#     n = len(coefficients) - 1
#     dx = (intervals[0][0] - intervals[1][0]) / 1000


def circle(x0: float = 0, y0: float = 0, r: float = 1,
           phi_1: float = 0, phi_2: float = 360, n: int = 10, reverse: int = 1):
    phi_1 = math.radians(phi_1)
    phi_2 = math.radians(phi_2)
    dphi = (phi_2 - phi_1) / n
    xy = []

    for i in list(range(0, n + 1)):
        xy.append((
            x0 + r * math.cos(phi_1 + i * dphi) * reverse,
            y0 + r * math.sin(phi_1 + i * dphi) * reverse
        ))

    return xy


def line_intersection(xy_slope: list):
    x1, x2 = xy_slope[0][0], xy_slope[1][0]
    y1, y2 = xy_slope[0][1], xy_slope[1][1]
    slope1, slope2 = math.radians(xy_slope[0][2]), math.radians(xy_slope[1][2])

    xp = y1 - y2 + x2 * math.tan(slope2) - x1 * math.tan(slope1)
    xp /= (math.tan(slope2) - math.tan(slope1))
    yp = y1 + math.tan(slope1) * (xp - x1)

    return xp, yp


if __name__ == "__main__":

    root_dir = os.getcwd()
    in_file = 'gv2_sec2.csv'
    out_dir = 'airfoils'
    out_dir = os.path.join(root_dir, out_dir)
    in_file = os.path.join(root_dir, in_file)

    CommonClass.create_dir(out_dir)

    blade_data = {}
    num_points = 50
    camber_line_bezier = []
    ps_bezier = []

    with open(in_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.split(sep=',')
            blade_data[line[0]] = float(line[1])

    chord = blade_data['b_ax'] / math.cos(math.radians(blade_data['gamma']))

    x0y0 = [
        (blade_data['r_le'], 0, blade_data['beta_in']),
        (blade_data['b_ax'] - blade_data['r_le'] - blade_data['r_te'],
         blade_data['b_ax'] + (blade_data['r_te'] -
                               blade_data['r_le']) *
         math.cos(math.radians(blade_data['gamma'])), blade_data['beta_out']
         )
    ]

    camber_line_cp = [
        x0y0[0][:-1],
        line_intersection(x0y0),
        x0y0[1][:-1]
    ]

    for i in range(num_points + 1):
        a = i / num_points
        camber_line_bezier.append(bezier_curve(camber_line_cp, a))

    camber_coefficients = bezier_coefficient(camber_line_cp)
