'''Import ROOT in such a way that it doesn't eat the arguments.

Borrowed from Chroma (http://bitbucket.org/chroma/chroma).
'''

import sys
_argv = sys.argv
sys.argv = []
import ROOT
ROOT.TObject
sys.argv = _argv
del _argv

