'''Counting statistics.'''

import math
import numpy as np
import scipy.stats

def poisson_zero_background(n, t, f, cl=0.9):
    '''Poisson regime counting experiment for the zero background case.

    From arxiv:1109.0494 Eq. 12 (CUORE)

    :param n: Number of atoms of isotope
    :param t: Live time in years
    :param f: Analysis signal efficiency
    :param cl: Confidence level
    :returns: Lifetime limit in years
    '''
    return -math.log(2) / math.log(1.0 - cl) * n * t * f


class FeldmanCousins():
    '''Find frequentist confidence intervals.
    
    Find confidence intervals according to the method proposed by Feldman and
    Cousins in "Unified approach to the classical statistical analysis of small
    signals" (Phys. Rev. D 57 7, 1998).

    This implementation build a lookup table given an expected background,
    allowing fast sampling as a function of observed counts.

    Note: Does not match Feldman-Cousins table values for cases where zero
    events are abserved.

    :param n_expected: The number of background events expected
    :param cl: Confidence level, e.g. 0.9 for a 90% CL
    :param mu_min: Minimum value of true parameter used for constructing bands
    :param mu_max: Maximum value of true parameter used for constructing bands
    :param mu_step: Size of sampling in true paramter mu
    '''
    def __init__(self, n_expected, cl=0.9,
                 mu_min=0.0, mu_max=50.0, mu_step=0.005):
        def poisexp(x, p):
            if p == 0:
                return scipy.stats.expon.pdf(x, p)
            else:
                return scipy.stats.poisson.pmf(x, p)

        n = np.arange(int(mu_max))
        self.mu = np.arange(mu_min, mu_max, mu_step)

        p = np.empty(shape=(len(self.mu), len(n)), dtype=np.float32)

        for i, m in enumerate(self.mu):
            p[i] = poisexp(n, m + n_expected)

        mu_best = (n - n_expected).clip(0) + n_expected

        d = np.empty_like(n, dtype=np.float32)
        for i, m in enumerate(mu_best):
            d[i] = poisexp(i, m)

        r = p / d

        ranks = np.empty_like(n)
        self.bands = np.empty(shape=(len(self.mu), 2), dtype=np.int32)

        for i in range(len(p)):
            ranks[r[i].argsort()] = np.arange(len(n))[::-1]
            prob = 0.0
            for jj, j in enumerate(ranks.argsort()):
                prob += p[i][j]
                if prob > cl:
                    break

            if prob < cl:
                band = [-1]
            else:
                band = n[(ranks >= 0) & (ranks <= jj)]

            self.bands[i] = [np.min(band), np.max(band)]

    def get_interval(self, n_observed):
        '''Get a confidence interval.

        :param n_observed: The number of events observed
        :returns: A (lower limit, upper limit) tuple
        '''
        interval = np.where((self.bands[:,0] >= 0) &
                            (self.bands[:,0] <= n_observed) &
                            (self.bands[:,1] >= n_observed))[0]
        return self.mu[interval[0]], self.mu[interval[-1]]


def bayesian_limit(observed, background, one_sided=False, sigma=0, cl=0.9,
                   mu_min=0.0, mu_max=250.0, step=0.01):
    '''Compute limits in a Bayesian way, with a likelihood function.

    Over-covers at low numbers of observed events, but converges to the
    frequentist limits in the high-N limit. Tis much faster than the full
    Feldman-Cousins calculation.

    :param observed: Number of events observed
    :param background: Expected number of background events
    :param one_sided: One- or two-sided interval?
    :param sigma: Gaussian uncertainty on the background expectation
    :param cl: Confidence level
    :param mu_min: Minimum true value to consider
    :param mu_max: Maximum true value to consider
    :param step: Step size in true parameter
    :returns: An upper limit if one_sided, else an interval as a tuple
    '''
    s = np.arange(mu_min, mu_max, step)
    if sigma > 0:
        b = np.arange(background - 5 * sigma,
                      background + 5 * sigma + 1e-9,
                      step).clip(0, np.inf)[np.newaxis].T
    else:
        b = background

    # The log likelihood function for a Poisson process
    ll = (-(s + b)
          - np.vectorize(math.lgamma)(observed + 1)
          + observed * np.log(s + b))

    # Constraints
    if sigma > 0:
        ll -= 0.5 * np.square(b - background) / np.square(sigma)

    likelihood = np.exp(ll)

    # Marginalize backgrounds
    if sigma > 0:
        likelihood = np.sum(likelihood, axis=0)

    # Extract points inside the confidence interval
    integral = np.cumsum(likelihood)
    integral /= integral[-1]

    if one_sided:
        return s[np.argmin(np.abs(integral - 0.9)) + 1]

    m = likelihood.argsort()[::-1]
    likelihood, s = likelihood[m], s[m]
    s = s[:np.searchsorted(integral, cl)+1]

    return np.min(s), np.max(s)

