'''Probability distributions, spectra, and functions.'''

import math
import numpy as np

ISR2PI = 1.0 / np.sqrt(2.0 * np.pi)

vlgamma = np.vectorize(math.lgamma)
'''Vectorized version of the math.lgamma log(gamma) function.'''


def erfinv(z):
    '''Inverse error function (for real z).

    Uses the Abramowitz and Stegun approximation; see
    http://en.wikipedia.org/wiki/Error_function.

    :param z: The argument (array-like)
    :returns: erf^-1(z), same shape as z
    '''
    a = 8.0 * (np.pi - 3) / (3 * np.pi * (4 - np.pi))
    x = 2.0 / (np.pi * a) + 0.5 * np.log(1 - np.square(z))
    s = np.sqrt(np.sqrt(np.square(x) - np.log(1-np.square(z)) / a) - x)
    return np.sign(z) * s


def gaussian(x, mu, s):
    '''Evaluate the Gaussian distribution.

        N(x; mu, s) = A * exp(-(x-mu)^2 / (2 * sigma)^2)

        A = 1 / (sigma * sqrt(2 * pi))

    :param x: Array-like, points at which to evaluate
    :param mu: Gaussian mean
    :param s: Gaussian standard deviation
    :returns: Array-like y-values, same shape as x
    '''
    return 1.0 / (s*ISR2PI) * np.exp(-0.5 * np.square((x-mu)/s))


def poisson(x, mu):
    '''Evaluate the Poisson distribution.

        Pois(x; mu) = mu^x * exp(-mu) / x!

    This works like ROOT's TMath::Poisson, using a Gamma function to
    interpolate for non-integer x.

    :param x: Array-like, points at which to evaluate
    :param mu: Poisson mean
    :returns: Array-like y-values, same shape as x
    '''
    return np.power(mu, x) * np.exp(-mu) / np.exp(vlgamma(x + 1))


def primakoff_rosen(e, q):
    '''Compute the Primakoff-Rosen approximation to the 2vbb spectrum.

        dN/dE = (E^4 + 10E^3 + 40E^2 + 60E + 30) * E * (Q-E)^5

    Q = decay endpoint, units are all in terms of electron mass

    :param e: Array-like, energies at which to evaluate
    :param q: 2vbb spectrum endpoint
    :returns: Un-normalized spectrum evaluated at e
    '''
    e = e / 0.511
    q = q / 0.511
    s = ((     np.power(e, 4) +
          10 * np.power(e, 3) +
          40 * np.power(e, 2) +
          60 * e +
          30) *
         e *
         np.power(q-e, 5))
    s[e > q] = 0
    return s


def apply_resolution(x, y, nhits, rebin_factor=4):
    '''Convolve with a Gaussian detector resolution function.

    N.B. This isn't careful with boundaries, or particularly fast.

    :param x: x values of unsmeared function
    :param y: y values of unsmeared function
    :param nhits: NHITs/MeV
    :param rebin_factor: Factor by which to oversample
    :returns: Smeared function, same shape as y
    '''
    x_os = np.linspace(x[0], x[-1], len(x) * rebin_factor)
    y_os = np.interp(x_os, x, y)
    y_out = np.zeros_like(y_os)
    sigma = np.sqrt(x_os / nhits)  # width as a function of energy

    for i in range(len(x_os)):
        g = y_os[i] * gaussian(x_os, x_os[i], max(1e-6, sigma[i]))
        for j in range(len(x_os)):
            y_out[j] += g[j]

    y_out *= (np.sum(y_os) / np.sum(y_out))
    return np.interp(x, x_os, y_out)

