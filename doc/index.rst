.. chocula documentation master file, created by
   sphinx-quickstart on Thu Jan 16 10:08:03 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Chocula's documentation!
===================================
Chocula is a collection of scripts and utilities for performing a single-bin
"counting" analysis to estimate the sensitivity of pretty-low background
search for pretty-rare physics processes, like neutrino-less double beta
decay.

Installation
------------
To install, run::

    $ python setup.py install

Quick Start
-----------
To perform a basic counting analysis, you'll need:

1. A data set. Currently chocula expects ROOT files with a specific format:
   a TTree named ``output`` and containing event energy in branch ``energy``;
   position in ``posx``, ``posy``, and ``posz``; and trigger index within an
   event in ``evIndex``, where untriggered events have ``evIndex == -1``,
   and retriggers have ``evIndex > 0``.
2. A CSV format background table with the following row format::

    name, ROOT LaTeX title, filename glob, rate/year, analysis scale factor

The CSV format allows comments with ``#`` and whitespace to format columns.
The filename glob is something like `/path/to/simulations/Ar42*.root`, with
the matching files having the format described above.

With these things in place, run::

    $ chocula mytable.csv

Contents:

.. toctree::
   :maxdepth: 2

   cli
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

