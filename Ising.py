import random
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import functions
import numpy as np
from scipy.optimize import curve_fit
import os
from functions import poly_fit


if __name__ == '__main__':
    size = 20
    time = 1000 * size ^ 2
    t = 0.05
    plot = False
    load = False
    if load:
        dipoles_orig = np.load('dipoles.npy')
        size = len(dipoles_orig)
        print(size)
    else:
        dipoles_orig = functions.create_system(size)
        print(dipoles_orig)

    energy_temp = []  # The energy will be one more than the iterations
    #fig, ax = plt.subplots(3)
    cv_temp = []
    counter = 0
    for t in np.arange(0.1, 10, 0.1):
        if counter % 10 == 0:
            print(counter)
        dipoles = dipoles_orig
        energy = [functions.calc_energy(dipoles)]
        cv = [functions.specific_heat(dipoles, t)]
        for _ in range(time):
            i = int(random.random() * size)
            j = int(random.random() * size)
            u = functions.calc_interaction(i, j, dipoles)
            dipoles = functions.flip_spin(i, j, u, t, dipoles)
            energy.append(functions.calc_energy(dipoles))
            cv.append(functions.specific_heat(dipoles, t))
            if plot:
                ax[0].cla()
                ax[1].cla()
                ax[2].cla()
                ax[0].set_title("frame {}".format(_))
                ax[0].imshow(dipoles)
                ax[1].plot(energy)
                ax[2].plot(cv)
                plt.pause(0.001)
        if plot:
            plt.show()

        average_energy = sum(energy[int(time*0.95):])/len(energy[int(time*.95):])
        energy_temp.append(average_energy)
        average_cv = sum(cv[int(time*0.95):])/len(cv[int(time*0.95):])
        cv_temp.append(average_cv)
        counter += 1
    x_val = range(len(energy_temp))
    fig1, ax1 = plt.subplots(2)
    parameters, covariance = curve_fit(poly_fit, x_val, energy_temp)
    ax1[0].plot(x_val, poly_fit(x_val, parameters[0], parameters[1], parameters[2], parameters[3]))
    ax1[1].scatter(x_val, energy_temp)
    plt.show()
