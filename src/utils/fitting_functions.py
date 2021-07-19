import logging

import numpy as np

logger = logging.getLogger()


def sigmoid(x, L, x0, k, b):
    y = L / (1 + np.exp(-k * (x - x0))) + b
    return y


def exp_func(x, a, b):
    return a * np.exp(b * x)


def expo_func(x, a, b):
    return np.exp(a * (x - b))


def exp_func1(x, b):
    return np.exp(b * x)


def Hill_sigmoidal_func(x, a, b, c):  # Hill sigmoidal equation from zunzun.com
    return a * np.power(x, b) / (np.power(c, b) + np.power(x, b))


def func1(x, a, b, c, d):
    return d + ((a - d) / (1 + (x / c) ** b))


def func2(x, a, b, c):
    return a / (1 + np.exp(-b * (x - c)))


def sigmoidal_func(x, a, b, c):
    return a / (1 + np.exp(-c * (x - b)))
