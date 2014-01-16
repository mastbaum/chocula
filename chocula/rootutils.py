'''Oh, ROOT...'''

import sys
from rootimport import ROOT

# A less-horrible sequential palette for ROOT
COLORS = [  1,  2, 3,  4, 797,  7,  8,  9, 11,  6,
           12, 29, 5, 30,  34, 38, 40, 42, 45, 46,
           49,  1, 2,  3,   4,  5,  6, 7 ]

def build_tcut(**kwargs):
    '''Construct a TCut string programmatically.

    Arguments are turned into:

        * bool: key or !key
        * tuple or list: key > value[0] && key < value[1]
        * others: key == value

    For example,

        build_tcut(scintFit=True, energy=(2,3))

    becomes

        'scintFit && energy > 2 && energy < 3'

    Also, a key 'radius' becomes 'sqrt(posx*posx+posy*posy+posz*posz)' for
    convenience.
    '''
    cut = ''

    for k, v in kwargs.items():
        # Fake a "radius" field
        if k == 'radius':
            k = 'sqrt(posx*posx + posy*posy + posz*posz)'

        if type(v) == bool:
            if not v:
                cut += '!'
            cut += k
        elif type(v) == tuple or type(v) == list:
            assert(len(v) == 2)
            cut += '%s > %f && %s < %f' % (k, v[0], k, v[1])
        else:
            cut += (k + ' == ' + str(v))

        cut += ' && '

    cut = cut[:-4]  # Trim off the final ' && '

    return cut


def get_energy_roi(signal, cut):
    '''Fit the signal energy with a Gaussian.

    :param signal: The signal to fit
    :param cut: A TCut expressing the cuts to apply
    :returns: A (mean, sigma) tuple
    '''
    name = '__h_roifit_%s' % signal.name
    if not hasattr(signal, 'tree'):
        raise Exception('Signal cannot be a chain.')

    signal.tree.Draw('energy>>%s' % name, cut)
    h = ROOT.gDirectory.Get(name)

    h.Fit('gaus', 'q')
    mean, sigma = (h.GetFunction('gaus').GetParameter(1),
                   h.GetFunction('gaus').GetParameter(2))
    h.Delete()

    return mean, sigma 


def setup_environment():
    '''Set up global defaults.'''
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)


def set_plot_options(h, color=1, ymin=0.01, ymax=1000):
    '''Set some common histogram options.

    :param h: The histogram
    :param color: The ROOT color ID
    :param ymin: Minimum on the Y axis
    :param ymax: Maximum on the Y axis
    :returns: None, just modifies the input in place
    '''
    h.SetDirectory(0)
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    w = h.GetXaxis().GetBinWidth(0)
    h.SetYTitle('Counts/bin')
    h.GetYaxis().SetRangeUser(ymin, ymax)
    h.SetMinimum(ymin)
    h.SetMaximum(ymax)
    h.SetXTitle('Energy (MeV)')
    h.GetXaxis().SetLabelFont(132)
    h.GetXaxis().SetTitleFont(132)
    h.GetXaxis().SetTitleSize(0.07)
    h.GetXaxis().SetLabelSize(0.07)
    h.GetXaxis().SetTitleOffset(1)
    h.GetYaxis().SetTitleSize(0.07)
    h.GetYaxis().SetLabelSize(0.07)
    h.GetYaxis().SetLabelFont(132)
    h.GetYaxis().SetTitleFont(132)
    h.GetYaxis().SetTitleOffset(1)

