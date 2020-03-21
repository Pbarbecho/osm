.. ovsm documentation master file, created by
   sphinx-quickstart on Tue Mar 17 11:23:33 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Automating large-scale simulations for OMNeT++
==============================================

OSM allows to OMNeT++ users to quickly and easily execute large-scale network simulations. Three shell commands (including help context) are available:

OSM on Github: `<https://github.com/Pbarbecho/osm>`_


.. code:: bash

  # Build and lauch the simulation campaign
  $ovsm launcher [OPTIONS] INIFILE MAKEFILE

  # Summarize result files located in output folder
  $ovsm parser [OPTIONS]

  # Analyze summarized file
  $ovsm analyzer [OPTIONS]


Feature highlights
------------------

* Supports Python >= 3.5;
* Fine grane control of the simulation campaign;
* Customizable/interactive plotting
* Runs parallelized simulations and post-processing for large number of files (common in large-scale simulations);


User's guide
------------
.. toctree::
   :maxdepth: 2

   installation
   cli

Code Documentation
--------------------
.. toctree::
   :maxdepth: 2

   modules