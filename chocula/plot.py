'''Utilities to do the plotting of events in a dataset.'''

import uuid
import multiprocessing
from chocula.rootutils import COLORS
from chocula.rootimport import ROOT

class _PlotSpecification(object):
    def __init__(self, nbins, xmin, xmax, live_time, color=1, cut=''):
        self.nbins = nbins
        self.xmin = xmin
        self.xmax = xmax
        self.live_time = live_time
        self.color = color
        self.cut = cut


def _plot_signal((signal, spec)):
    return signal.plot(spec.nbins, spec.xmin, spec.xmax,
                       spec.color, spec.live_time, spec.cut)


def _make_legend():
    l = ROOT.TLegend(0.05, 0.1, 0.9, 0.9)
    l.SetBorderSize(0)
    l.SetFillColor(0)
    l.SetTextSize(0.08)
    l.SetTextFont(132)
    return l


def _make_split_canvas():
    c = ROOT.TCanvas('canvas', 'canvas', 600, 350)
    pad2 = ROOT.TPad('pad2', 'pad2', 0.762, 0.005, 0.99, 0.995)
    pad1 = ROOT.TPad('pad1', 'pad1', 0.005, 0.005, 0.8, 0.995)
    pad1.SetBottomMargin(0.15)
    pad1.SetLeftMargin(0.2)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy()
    pad1.SetTicks(0, 2)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    return c, pad1, pad2


def plot(signals, nbins, xmin, xmax, ymin, ymax, live_time=1, cut='',
         sums=True, processes=None):
    '''Create a plot of the energy distributions for all the signals.

    :param signals: List of Signals and Chains
    :param nbins: Number of energy bins
    :param xmin: Minimum energy
    :param xmax: Maximum energy
    :param ymin: Minimum y value
    :param ymax: Maximum y value
    :param live_time: Live time used to scale plot
    :param cut: A ROOT TCut string
    :param sums: Show summed spectrum in plot
    :param processes: Number of parallel processes
    :returns: A (canvas, legend, [plots]) tuple with all the histograms
    '''
    print sums
    if processes is None:
        processes = multiprocessing.cpu_count()

    specs = []
    for i in range(len(signals)):
        specs.append(_PlotSpecification(nbins, xmin, xmax, live_time,
                                        color=COLORS[i], cut=cut))
    signal_spec = zip(*(signals, specs))

    if processes > 1:
        pool = multiprocessing.Pool(processes)
        plots = pool.map(_plot_signal, signal_spec)
    else:
        plots = []
        for o in signal_spec:
            plots.append(_plot_signal(o))

    canvas, plot_pad, legend_pad = _make_split_canvas()
    legend = _make_legend()

    signal_plots = zip(*(signals, plots))

    # Summed spectra
    hsum = plots[0].Clone('__hsum_%s' % uuid.uuid4().hex[-10:])
    hsum.Reset()
    hsum.SetLineWidth(3)
    hsum.SetLineColor(ROOT.kBlack)
    hsum_bkg = plots[0].Clone('__hsum_%s' % uuid.uuid4().hex[-10:])
    hsum_bkg.Reset()
    hsum_bkg.SetLineWidth(3)
    hsum_bkg.SetLineColor(ROOT.kBlack)
    hsum_bkg.SetLineStyle(2)

    if sums:
        legend.AddEntry(hsum, 'Sum')
        legend.AddEntry(hsum_bkg, 'Sum, background')

    # Build legend and sums
    for signal, plot in signal_plots:
        legend.AddEntry(plot, signal.title)
        hsum.Add(plot)
        if signal.chain != 'S':
            hsum_bkg.Add(plot)

    legend_pad.cd()
    legend.Draw()

    # Draw
    plot_pad.cd()
    for i, (signal, plot) in enumerate(reversed(signal_plots)):
        plot.Draw('' if i==0 else 'same')
        if ymin is not None and ymax is not None:
            plot.SetMinimum(ymin)
            plot.SetMaximum(ymax)

    if sums:
        hsum.Draw('same')
        plots.append(hsum)
        hsum_bkg.Draw('same')
        plots.append(hsum_bkg)

    return canvas, legend, plots

