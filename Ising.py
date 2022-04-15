import random
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import functions
import numpy as np
from scipy.optimize import curve_fit
import os
from functions import poly_fit, inverse_square_fit


if __name__ == '__main__':
    size = 20
    time = 1000 * size ^ 2
    discard_ratio = 0.1
    plot = False
    load = False
    t_range = np.arange(0.1, 10, 0.1)

    if load:
        dipoles_orig = np.load('dipoles.npy')
        size = len(dipoles_orig)
        print(size)
    else:
        dipoles_orig = functions.create_system(size)
        print(dipoles_orig)

    energy_temp = []  # The energy will be one more than the iterations
    cv_temp = []
    for counter, t in enumerate(t_range):
        if counter % 10 == 0:
            print(counter)
        dipoles = dipoles_orig
        energy, cv = functions.loop(dipoles, t, time)

        average_energy = sum(energy[int(time*discard_ratio):])/len(energy[int(time*discard_ratio):])
        energy_temp.append(average_energy)
        average_cv = sum(cv[int(time*discard_ratio):])/len(cv[int(time*discard_ratio):])
        cv_temp.append(average_cv)

    fig, ax = plt.subplots(3)
    parametersE, covarianceE = curve_fit(poly_fit, t_range, energy_temp)
    parametersC, parametersC = curve_fit(inverse_square_fit, t_range, cv_temp)
    ax[0].plot(t_range, poly_fit(t_range, parametersE[0], parametersE[1], parametersE[2], parametersE[3]), color='blue')
    ax[0].scatter(t_range, energy_temp, color='red')
    ax[0].set(xlabel='Temperature', ylabel='E/dipole')
    ax[1].scatter(t_range, cv_temp, color='red')
    ax[1].set(xlabel='Temperature', ylabel='Specific Heat / Dipole')
    ax[2].set(xlabel='Temperature', ylabel='Entropy / Dipole')
    print((len(t_range), len(cv_temp)))
    ax[2].scatter(t_range[1:], functions.entropy(cv_temp, t_range))
    plt.show()

