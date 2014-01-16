Count:Chocula
=============
A collection of scripts and utilities for performing a single-bin "counting"
analysis to estimate the sensitivity of pretty-low background searches for
pretty-rare physics processes, like neutrino-less double beta decay.

Documentation
-------------
API and user documentation is available in the `doc` directory.

Installation
------------
To install, run:

    $ python setup.py install

Quick Start
-----------
To perform a basic counting analysis, you'll need:

1. A data set. Currently chocula expects ROOT trees with a specific format:
   named "output" and containing event energy in branch "energy"; position
   in "posx", "posy", and "posz"; and trigger index within an event in
   "evIndex", where untriggered events have evIndex == -1, and retriggers have
   evIndex > 0.
2. A CSV background table with the following row format:

    name, ROOT LaTeX title, filename glob, rate/year, analysis scale factor

The filename glob is something like `/path/to/simulations/Ar42*.root`, and
the matching files have the format described.

With these things in place, run:

    $ ./bin/chocula mytable.csv

