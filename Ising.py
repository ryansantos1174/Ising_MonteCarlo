import random
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import functions
import numpy as np
from scipy.optimize import curve_fit
import os
from functions import poly_fit, inverse_square_fit

if __name__ == '__main__':
    size = 8
    time = 100 * (size ** 2)
    discard_ratio = 0.8
    plot = False
    load = True
    const_temp = True
    t_range = np.arange(0.1, 5, 0.1)
    t = 10

    if load:
        dipoles_orig = np.load('dipoles.npy')
        size = len(dipoles_orig)
        print(size)
    else:
        dipoles_orig = functions.create_system(size)
        np.save('dipoles.npy', dipoles_orig)
        print(dipoles_orig)
    # Empty arrays that I append my plotting functions to
    energy_temp = []
    cv_temp = []
    xi = []
    mag = []
    cor = []

    if const_temp:
        dipoles = dipoles_orig
        # The loop function runs the monte carlo simulation
        energy, _, _, magnet, _ = functions.loop(dipoles, t, time, plot=True, hist=True, sym_break=True)
        average_energy = sum(energy[int(time * discard_ratio):]) / len(energy[int(time * discard_ratio):])
        energy_temp.append(average_energy)
        # average_cv = sum(cv[int(time * discard_ratio):]) / len(cv[int(time * discard_ratio):])
        # cv_temp.append(average_cv)
    else:
        for counter, t in enumerate(t_range):
            if counter % 10 == 0:
                print(counter)
            dipoles = dipoles_orig
            energy, cv, Chi, magnet, _ = functions.loop(dipoles, t, time, hist=False, sym_break=False)
            average_energy = sum(energy[int(time * discard_ratio):]) / len(energy[int(time * discard_ratio):])
            energy_temp.append(average_energy)
            average_cv = sum(cv[int(time * discard_ratio):]) / len(cv[int(time * discard_ratio):])
            average_chi = sum(Chi[int(time * discard_ratio):]) / len(Chi[int(time * discard_ratio):])
            average_magnet = sum(magnet[int(time * discard_ratio):]) / len(magnet[int(time * discard_ratio):])
            xi.append(average_chi)
            cv_temp.append(average_cv)
            mag.append(average_magnet)


# Creating the Plots
# plt.scatter(t_range, energy_temp, color='red')
# plt.xlabel('Temperature (epsilon/K)')
# plt.ylabel('Energy/dipole')
# plt.show()
# plt.savefig('./Plots/E_T.png')
# #
# plt.scatter(t_range, cv_temp, color='red')
# plt.xlabel('Temperature (epsilon/K)')
# plt.ylabel('Specific Heat / Dipole')
# plt.show()
# plt.savefig('./Plots/cv_T.png')
#
# plt.scatter(t_range[1:], functions.entropy(cv_temp, t_range))
# plt.xlabel('Temperature')
# plt.ylabel('Entropy / Dipole')
# plt.show()
# plt.savefig('./Plots/S_T.png')

# fig, ax = plt.subplots(2)
# ax[0].scatter(t_range, mag, color='green' )
# ax[1].scatter(t_range, xi, color='black')
# plt.show()

# plt.scatter(t_range, xi, color='black')
# plt.xlabel('Temperature(epsilon/K)')
# plt.ylabel('Susceptibility')
# plt.show()
# plt.savefig('./Plots/Susceptibility.png')
#
# plt.scatter(t_range, mag, color='black')
# plt.xlabel('Temperature(epsilon/K)')
# plt.ylabel('Magnetization/ Dipole')
# plt.show()
# plt.savefig('./Plots/Magnetization.png')
