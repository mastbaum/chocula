'''Counting statistics.'''

import math

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

