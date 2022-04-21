import numpy as np
import random
from math import exp, sqrt, fabs
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import matplotlib.animation as animation


def calc_interaction(i, j, h, array, sym_break=False):
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
    if sym_break:
        ediff = 2 * array[i, j] * (top + bottom + left + right) - (2 * h * array[i, j])
    else:
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


# Gives the energy per particle
def calc_energy(array, h=0.1):
    energy = 0
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
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
            energy += -(left * right * bottom * top) * array[i,j]
    energy = (energy/2) - h * np.sum(array)
    energy = energy/get_items(array)
    return energy


def specific_heat(array, t):
    e_sq_avg = np.sum(np.square(array)) / get_items(array)
    e_avg_sq = (np.sum(array) / get_items(array)) ** 2
    cv = (e_sq_avg - e_avg_sq) / (t ** 2)
    return cv


def entropy(sp_heat, t):
    integrand = []
    y_value = []
    for i, val in enumerate(sp_heat):
        try:
            integrand.append((val/t[i]) * (t[i+1]-t[i]))
            y_value.append(sum(integrand))
        except IndexError:
            pass
    return y_value


def poly_fit(x, a, b, c, d):
    y_list = []
    for val in x:
        y = a + b * val + c * val ** 2 + d * val ** 3
        y_list.append(y)
    return y_list


def inverse_square_fit(x, a, b, c):
    y_list = []
    for val in x:
        y = (a / ((b * val + c)**2))
        y_list.append(y)
    return y_list


def exponential_fit(x, a, xi):
    return a*np.exp(-x / xi)


def magnetization(array):
    length = get_items(array)
    m = np.sum(array)/ length
    m_square = np.sum(np.square(array)) / length
    return m_square, m


# Setting k=1
def chi(array, t):
    length = get_items(array)
    m_square, m = magnetization(array)
    susceptibility = (m_square - (m ** 2)) / t
    return susceptibility / length
def calc_distance(pt1, pt2):
    d = sqrt((pt1[0] - pt2[0])**2 + (pt1[1]-pt2[1])**2)
    return d


def spin_spin_correlation(array):
    length = array.shape[0]
    _, m = magnetization(array)
    correlation_length = []
    for r in range(array.shape[0]):
        counter = 0
        values = []
        for j in range(array.shape[0]):
            for i in range(array.shape[1]):
                if i+r < array.shape[0]:
                    values.append(array[i, j] * array[i + r, j])
                else:
                    None
                if i-r >= 0:
                    values.append(array[i, j] * array[i-r, j])
                else:
                    None
                if j+r < array.shape[1]:
                    values.append(array[i, j] * array[i, j+r])
                else:
                    None
                if j-1 >= 0:
                    values.append(array[i, j] * array[i, j-r])
                else:
                    None
                counter += 1
        corr = sum(values)
        # Will take the average of the correlation between the two points
        correlation = corr / counter
        # Subtracts off average magnetization
        correlation = correlation - (m ** 2)
        correlation_length.append((correlation, r))
    return correlation_length


def corr_length(correlation):
    y_values = [item[0] for item in correlation]
    x_values = [item[1] for item in correlation]
    popt, _ = curve_fit(exponential_fit, x_values, y_values)
    return popt[1]


def loop(array, t, time, plot=False, hist=False, sym_break=False):
    size = array.shape[0]
    energy = [calc_energy(array)]
    cv = [specific_heat(array, t)]
    Chi = [chi(array, t)]
    m_square, m = magnetization(array)
    magnet = [m]
    images = [array]
    for _ in range(time):
        plt.clf()
        i = int(random.random() * size)
        j = int(random.random() * size)
        u = calc_interaction(i, j, 0.1, array, sym_break=sym_break)
        array = flip_spin(i, j, u, t, array)
        energy.append(calc_energy(array, 0))
        cv.append(specific_heat(array, t))
        Chi.append(chi(array, t))
        m_square, m = magnetization(array)
        magnet.append(m)
        images.append(array)
    if hist:
        plt.clf()
        fig, ax = plt.subplots(2)
        ax[0].set(xlabel=f'Energy (T={t})', ylabel=f'Count (sweeps={time})')
        ax[1].set(xlabel=f'Magnetization (T={t})', ylabel=f'Count (sweeps={time})')
        ax[0].hist(energy)
        ax[1].hist(magnet)
        plt.subplots_adjust(hspace=0.2, wspace=0.2)
        plt.savefig(f'./q_hist_{t}.png')
    if plot:
        plt.clf()
        plt.imshow(array)
        plt.title(f'Figsize = {size} x {size}')
        plt.savefig(f'./image_{t}.png')

    corr = spin_spin_correlation(array)
    xi = corr_length(corr)
    return energy, cv, Chi, magnet, corr, xi

# The way I have calc_energy setup it also works for the magnetization







