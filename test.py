import numpy as np
from functions import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x =[1,2,3,4]
y=[1,4,9,16]


def func(x, a):
    return a*x**2


popt, a = curve_fit(func, x, y)


