Library API
===========
Chocula includes many handy utilities in addition to the CLI tools, for
creating your own counting analysis.

Utilities
---------
Statistics
``````````
.. automodule:: chocula.stats
   :members:

Tools
`````
.. automodule:: chocula.tools
   :members:

ROOT Utilties
`````````````
.. automodule:: chocula.rootutils
   :members:

Dataset Loading
```````````````
.. automodule:: chocula.loader
   :members:

Counting
````````
.. automodule:: chocula.counting
   :members:

Distributions
`````````````

.. automodule:: chocula.distributions
   :members:

Plotting
````````

.. automodule:: chocula.plot
   :members:

Signals
-------
Signals (including both backgrounds and the signal of interest) are represented
in two types of objects, ``Signal``s and ``Chains``, where the latter is a
collection of signals treated as a unit.

Signals have an underlying dataset in the form of a ROOT tree, which is loaded
from disk on demand.

.. automodule:: chocula.signals
   :members:

Nuclear Data
------------
.. automodule:: chocula.nuclei
   :members:

