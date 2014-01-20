import multiprocessing
from rootimport import ROOT
from chocula import rootutils

class Signal(object):
    '''A container for a signal or background.

    :param name: A string identifier
    :param chain: Name of a chain that this signal belongs to
    :param title: A ROOT LaTeX title
    :param filename: Filename to load for data
    :param rate: Number of events per year
    :param scale: Analysis scaling factor
    :param autoload: Load the ROOT dataset automatically
    '''
    def __init__(self, name, chain, title, filename, rate, scale=1.0,
                 autoload=False):
        self.name = name
        self.chain = chain
        self.title = title
        self.filename = filename
        self.rate = rate
        self.scale = scale
        self.normalization = self.rate * self.scale

        # Set by load_dataset
        self.tree = None
        self.mc_events = 0

        if autoload:
            load_dataset()

    def load_dataset(self, branch_name='output'):
        '''Load a ROOT data set from files.

        :param branch_name: Name of the TNtuple branch to read
        '''
        print 'Loading dataset for', self.name
        self.tree = ROOT.TChain(branch_name)
        self.tree.Add(self.filename)
        list_name = '__mc_events_%s' % self.name
        self.tree.Draw('>>%s' % list_name, 'evIndex == 0 || evIndex == -1')
        event_list = ROOT.gDirectory.Get(list_name)
        self.mc_events = event_list.GetN()

    def count(self, cut=''):
        '''Get the rate of the events that pass a cut.

        :param cut: A ROOT TCut string
        :returns: The rate of events per year that pass the cut
        '''
        list_name = '__roi_events_%s' % self.name
        self.tree.Draw('>>%s' % list_name, cut)
        roi_events = ROOT.gDirectory.Get(list_name)
        counts = self.normalization * roi_events.GetN() / self.mc_events
        return [(self.name, counts)]

    def plot(self, nbins, xmin, xmax, color=1, live_time=1, cut='',
             e_units='MeV'):
        '''Plot the energy distribution into a 1D histogram.

        :param nbins: Number of energy bins
        :param xmin: Minimum of domain
        :param xmax: Maximum of domain
        :param color: ROOT color ID
        :param live_time: Scale factor for live time (years)
        :param cut: A ROOT TCut string
        :param e_units: Energy units (if not MeV)
        :returns: The energy spectrum as a scaled TH1F
        '''
        name = '__energy_hist_%s' % self.name
        h = ROOT.TH1F(name, '', nbins, xmin, xmax)
        binsize = '%1.1f' % (h.GetBinWidth(1) * 1000)
        h.SetXTitle('Energy (' + e_units + ')')
        h.SetYTitle('Counts/' + str(live_time) + ' y/' + binsize + ' keV bin')
        self.tree.Draw('energy>>%s' % name, cut)
        rootutils.set_plot_options(h, color)
        if h.Integral() > 0:
            pass_cut = h.Integral() / self.mc_events
            h.Scale(self.normalization * live_time * pass_cut / h.Integral())
        return h


class Chain(object):
    '''A group ("chain") of related signals that are treated as a unit.

    :param name: A string identifier
    :param title: A ROOT LaTeX title
    '''
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.chain = None
        self.signals = []

    def add_signal(self, signal):
        '''Add a signal to the background chain.

        :param signal: The Signal (or Chain) object
        '''
        self.signals.append(signal)

    def count(self, cut=''):
        '''Get the rate of the events that pass a cut.

        :param cut: A ROOT TCut string
        :returns: A list of (name, counts) tuples for all signals in the chain
        '''
        counts = []
        for signal in self.signals:
            counts.extend(signal.count(cut))
        return counts

    def plot(self, nbins, xmin, xmax, color=1, live_time=1, cut='',
             e_units='MeV'):
        '''Plot the energy distribution for an entire chain into a single 1D
        histogram.

        :param nbins: Number of energy bins
        :param xmin: Minimum of domain
        :param xmax: Maximum of domain
        :param color: ROOT color ID
        :param live_time: Scale factor for live time (years)
        :param cut: A ROOT TCut string
        :param e_units: Energy units (if not MeV)
        :returns: The energy spectrum as a scaled TH1F
        '''
        name = '__energy_hist_%s' % self.name
        hsum = ROOT.TH1F(name, '', nbins, xmin, xmax)
        binsize = '%1.1f' % (hsum.GetBinWidth(1) * 1000)
        hsum.SetXTitle('Energy (' + e_units + ')')
        hsum.SetYTitle('Counts/' + str(live_time) + ' y/' +
                       binsize + ' keV bin')

        for signal in self.signals:
            h = signal.plot(nbins, xmin, xmax, live_time=live_time,
                            cut=cut, e_units=e_units)
            hsum.Add(h)

        rootutils.set_plot_options(hsum, color)
        return hsum
        

