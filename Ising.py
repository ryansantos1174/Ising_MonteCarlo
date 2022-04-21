import random
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import functions
import numpy as np
from scipy.optimize import curve_fit
import os
from functions import poly_fit, inverse_square_fit, exponential_fit

if __name__ == '__main__':
    size = 10
    time = 100 * (size ** 2)
    discard_ratio = 0.8
    load = False
    t_range = np.arange(0.1, 5, 0.01)
    t = 2.7

    if load:
        dipoles_orig = np.load('dipoles.npy')
        size = len(dipoles_orig)
        print(size)
    else:
        dipoles_orig = functions.create_system(size)
        np.save('dipoles2.npy', dipoles_orig)
        print(dipoles_orig)
    # Empty arrays that I append my plotting functions to

    energy_temp = []
    cv_temp = []
    chi_array = []
    mag = []
    cor = []

    for counter, t in enumerate(t_range):
        if counter % 10 == 0:
            print(counter)
        dipoles = dipoles_orig
        energy, cv, _, _, _ , _= functions.loop(dipoles_orig, t, time)
        energy_sym, _, Chi, magnet, _, xi = functions.loop(dipoles_orig, t, time, sym_break=True)
        average_energy = sum(energy[int(time*discard_ratio):])/len(energy[int(time*discard_ratio):])
        average_magnet = sum(magnet[int(time * discard_ratio):]) / len(magnet[int(time * discard_ratio):])
        energy_temp.append(average_energy)
        average_cv = sum(cv[int(time*discard_ratio):])/len(cv[int(time*discard_ratio):])
        average_chi = sum(Chi[int(time * discard_ratio):]) / len(Chi[int(time * discard_ratio):])
        cv_temp.append(average_cv)
        mag.append(average_magnet)
        chi_array.append(average_chi)
        cor.append(xi)

    temps = [1, 2, 2.7, 4, 8]
    for tp in temps:
        _, _, _, _, _, _ = functions.loop(dipoles_orig, tp, time, plot=True, hist=True, sym_break=True)
    plt.clf()
    plt.scatter(t_range, energy_temp, color='red')
    plt.xlabel(r'Temperature ($\epsilon / K)')
    plt.ylabel('Energy / Dipole')
    plt.savefig('./q1_E.png')

    plt.clf()
    plt.scatter(t_range, cv_temp, color='red')
    plt.xlabel(r'Temperature ($\epsilon / K)')
    plt.ylabel('Specific Heat / Dipole')
    plt.savefig('./q1_cv.png')

    plt.clf()
    plt.scatter(t_range[1:], functions.entropy(cv_temp, t_range))
    plt.xlabel(r'Temperature ($\epsilon / K)')
    plt.ylabel('Entropy / Dipole')
    plt.savefig('./q1_s.png')

    plt.clf()
    plt.scatter(t_range, chi_array, color='black')
    plt.xlabel(r'Temperature($\epsilon / K)')
    plt.ylabel('Susceptibility')
    plt.savefig('./Susceptibility.png')

    plt.clf()
    plt.scatter(t_range, mag, color='black')
    plt.xlabel(r'Temperature($\epsilon / K)')
    plt.ylabel('Magnetization/ Dipole')
    plt.savefig('./Magnetization.png')

    plt.clf()
    plt.scatter(t_range, cor, color='black')
    plt.xlabel(r'Temperature($\epsilon / K)')
    plt.ylabel('Correlation Length')
    plt.savefig('./CorrelationLength.png')




