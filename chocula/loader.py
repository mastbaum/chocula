'''Load datasets for analysis.'''

import csv
import multiprocessing
from chocula.signals import Signal, Chain

# Names of background chains
chains = {
    'U': 'U Chain',
    'Th': 'Th Chain',
    'E': 'External',
    'C': 'Cosmogenics',
    'BiPo214': '^{214}Bi + ^{214}Po',
}

def import_csv(csv_file):
    '''Load a list of datasets from a CSV file.

    :param csv_file: Filename or file object
    :returns: List of Signals
    '''
    if not isinstance(csv_file, file):
        csv_file = open(csv_file, 'r')

    reader = csv.reader(filter(lambda row: row[0] != '#', csv_file))
    signals = []

    for row in reader:
        row = map(lambda x: x.strip(), row)
        chain, name, title, filename, scale, rate_y1, rate_y2, rate_y3, rate_y4, rate_y5 = row
        rates = map(float, [rate_y1, rate_y2, rate_y3, rate_y4, rate_y5])
        scale = float(scale)
        signal = Signal(name, chain, title, filename, rates, scale=scale)
        signals.append(signal)

    csv_file.close()
    return signals


def _load_signal_dataset(signal):
    signal.load_dataset()
    return signal


def load(signals, processes=None):
    '''Load signal parameters and ROOT datasets.

    :param signals: A list of Signals, or a file with signals
    :param processes: Load datasets in parallel processes
    :returns: The list of Signals and Chains
    '''
    # If we have a file or filename, load from CSV
    if isinstance(signals, str) or isinstance(signals, file):
        signals = import_csv(signals)

    if processes is None:
        processes = multiprocessing.cpu_count()

    if processes > 1:
        pool = multiprocessing.Pool(processes)
        signals = pool.map(_load_signal_dataset, signals)
    else:
        for signal in signals:
            signal.load_dataset()

    # Build a list of signals with the chains merged into Chains
    chained = []
    for signal in signals:
        if signal.chain is None or signal.chain == '' or signal.chain == 'S':
            chained.append(signal)
        else:
            try:
                c = filter(lambda x: x.name == signal.chain, chained)[0]
                c.add_signal(signal)
            except IndexError:
                c = Chain(signal.chain, chains[signal.chain])
                c.add_signal(signal)
                chained.append(c)

    return chained

