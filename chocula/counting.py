'''Utilities to do the counting of events in a dataset.'''

import itertools
import multiprocessing

def _count_signal((signal, cut)):
    return signal.count(cut=cut)

def count(signals, cut, processes=None):
    '''Count the number of events that pass a cut.

    :param signals: List of Signals and Chains
    :param cut: A ROOT TCut string
    :param processes: Number of parallel processes
    :returns: A dict with the counts for each signal
    '''
    counts = []

    if processes is None:
        processes = multiprocessing.cpu_count()

    if processes > 1:
        pool = multiprocessing.Pool(processes)

        # Cannot give multiple arguments to multiprocessing's map, so create a
        # list of (signal, cut) tuples and pass those to the mapping function
        signal_cut = itertools.product(signals, [cut])
        individual_counts = pool.map(_count_signal, signal_cut)

        counts = [item for sublist in individual_counts for item in sublist]
    else:
        for signal in signals:
            counts.extend(signal.count(cut=cut))

    return counts

