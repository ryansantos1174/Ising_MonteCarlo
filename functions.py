import numpy as np
import random
from math import exp, tanh


def calc_interaction(i, j, array):
    # Getting the left value
    if i == 0:
        left = array[-1, j]
    else:
        left = array[i - 1, j]
    # Getting right value
    if i == array.shape[0] - 1:
        right = array[0, j]
    else:
        right = array[i + 1, j]
    # Top Value
    if j == 0:
        top = array[i, -1]
    else:
        top = array[i, j - 1]
    # Bottom Value
    if j == array.shape[0] - 1:
        bottom = array[i, 0]
    else:
        bottom = array[i, j + 1]
    ediff = 2 * array[i, j] * (top + bottom + left + right)
    return ediff


def create_system(size):
    array = np.ones((size, size))
    for j, row in enumerate(array):
        for i, item in enumerate(row):
            spin = random.choice([-1, 1, -1, -1])
            array[i, j] = spin * array[i, j]
    return array


def flip_spin(i, j, u, t, array):
    # T is defined as k*T
    rand = random.random()
    prob = exp(-u / t)
    if prob > rand:
        array[i, j] = array[i, j] * -1
    return array


def get_items(array):
    size = 1
    for dim in np.shape(array): size *= dim
    return size


def calc_energy(array):
    return np.sum(array) / get_items(array)


def specific_heat(array, t):
    k = 1.38e-23
    e_sq_avg = np.sum(np.square(array)) / get_items(array)
    e_avg_sq = (np.sum(array) / get_items(array)) ** 2
    cv = k * (e_sq_avg - e_avg_sq) / (t ** 2)
    return cv


def poly_fit(x, a, b, c, d):
    y_list = []
    for val in x:
        y = a + b * val + c * val ** 2 + d * val ** 3
        y_list.append(y)
    return y_list




