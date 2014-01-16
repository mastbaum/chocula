CLI Utilities
=============
``chocula``
-----------
The ``chocula`` utility reads a background table from a file, loads the ROOT
datasets, and counts events that pass cuts specified on the command line.

Usage
`````
::

    usage: chocula [-h] [--radius RADIUS] [--energy ENERGY] [--fitter FITTER]
                   [--processes PROCESSES] [--output OUTPUT]
                   table
    
    Counting experiment
    
    positional arguments:
      table                 Filename of background table
    
    optional arguments:
      -h, --help            show this help message and exit
      --radius RADIUS, -r RADIUS
                            Fiducial volume radius cut (mm)
      --energy ENERGY, -e ENERGY
                            Energy ROI as type or explicit "low:high"
      --fitter FITTER, -f FITTER
                            Vertex fitter
      --processes PROCESSES, -p PROCESSES
                            Number of parallel proceses
      --output OUTPUT, -o OUTPUT
                            Output CSV filename for counts

The energy ROI may be specified explicitly as ``--energy low:high``, or it
can be calculated automatically based on a Gaussian fit to the signal energy
distribution. To use this method, include the signal in the background table
with a chain "S" and use one of the following arguments to ``--energy``::

    fwhm    Full-width at half maximum
    hwhm    Asymmetric half-width at half maximum, the upper half of FWHM
    full    1 sigma below the mean to 1 sigma above
    upper   Mean to 1 sigma above
    m05p15  1/2 sigma below the mean to 3/2 sigma above the mean

The number of parallel processes defaults to the number of CPUs. Data files are
loaded in and counting is done in parallel. Note that this may not speed things
up, or even cause issues, if data files are on a slow network disk. Setting
``--processes 1`` completely disables all multiprocessing.

