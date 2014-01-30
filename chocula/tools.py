'''Tools to make counting easier.'''

import math

m_e = 511e3  # electron mass in eV

def lifetime_to_mass(isotope, lifetime):
    '''Convert a lifetime limit to a mass limit.

    :param isotope: Isotope object with nuclear parameters
    :param lifetime: Lifetime limit in years
    :returns: Mass limit in eV
    '''
    return m_e / math.sqrt(lifetime * isotope.G * isotope.M**2)


def mass_to_lifetime(isotope, mass):
    '''Convert a mass limit to a lifetime limit.

    :param isotope: Isotope object with nuclear parameters
    :param mass: Mass limit in eV
    :returns: Lifetime limit in years
    '''
    return 1.0 / (isotope.G * isotope.M**2 * (mass / m_e)**2)


def counts_to_lifetime(n, t, f, counts):
    '''Convert a limit in counts to a lifetime limit.

    :param n: Number of atoms of isotope
    :param t: Live time in years
    :param f: Analysis signal efficiency
    :param counts: Limit in counts
    :returns: Limit in years
    '''
    return math.log(2) * n * t * f / counts


def lifetime_to_counts(n, t, f, lifetime):
    '''Convert a limit in lifetime to a limit in counts.

    :param n: Number of atoms of isotope
    :param t: Lifetime in years
    :param f: Analysis signal efficiency
    :param lifetime: Lifetime limit in years
    :returns: Limit in counts
    '''
    return math.log(2) * n * t * f / lifetime

