'''A table of nuclear data.

Data is loaded in from a CSV table and becomes attributes of this module. For
example, the 'te130' row becomes thismodule.te130, an Isotope object.
'''

import os
import sys
import csv
import chocula.data

# This module, "self"
nuclei = sys.modules[__name__]

# The path to the nuclear data
data_path = os.path.split(chocula.data.__file__)[0]
nuclear_data_path = os.path.join(data_path, 'nuclei.csv')

class Isotope(object):
    '''Container for various nuclear parameters.

    :param Z: Atomic number
    :param A: Atomic mass
    :param g_A: 0vbb phase space factor
    :param M: 0vbb matrix element
    '''
    def __init__(self, Z, A, g_A, M):
        self.Z = Z
        self.A = A
        self.g_A = g_A
        self.M = M


def load_table():
    '''Load nuclear data from a CSV table and make a dict out of it.'''
    data_file = file(nuclear_data_path)
    reader = csv.reader(filter(lambda row: row[0] != '#', data_file))
    isotopes = {}
    for row in reader:
        row = map(lambda x: x.strip(), row)
        name, Z, A, g_A, M = row
        isotopes[name] = Isotope(Z, A, g_A, M)
    return isotopes


_table_isotopes = load_table()
available_isotopes = _table_isotopes.keys()

for name, isotope in _table_isotopes.items():
    setattr(nuclei, name, isotope)

