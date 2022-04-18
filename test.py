import numpy as np
from functions import *
import matplotlib.pyplot as plt

dipoles = create_system(100)

c = spin_spin_correlation(dipoles)
plt.plot(c[:][0], c[:][1])
plt.show()
