<p align="center">
  <img src="doc/logo.png" width="400">
</p>

# Automating OMNeT++ simulations #

OSM allows to OMNeT++ users to quickly and easily execute large-scale network simulations. 
This is an automation tool for OMNeT++ large-scale simulations and data analysis.
Based on OMNeT++ structure, this tool reads .ini file and build simulation campaign.
Users' manual an code documentation is available at [readthedocs][rtd].

OSM tool includes the following tool:    
```bash
  - Launcher: build simulation campaign and execute parallel simulations in batches.
  - Parser:   Automatically try to detect output results files from simulation campaign (.vec,.sca, custom format) and convert those to an unique output file. 
  - Analyzer: Reads parsed files and plot results from template or launch an interactive plot in a web browser (pyvot tables). 
```

```bash
  # Build and lauch the simulation campaign
  $ovsm launcher [OPTIONS] INIFILE MAKEFILE

  # Summarize result files located in output folder
  $ovsm parser [OPTIONS] 

  # Analyze summarized file 
  $ovsm analyzer [OPTIONS] 
```

[![Documentation Status](https://readthedocs.org/projects/osm/badge/?version=latest)](https://osm.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Pbarbecho/osm/branch/master/graph/badge.svg)](https://codecov.io/gh/Pbarbecho/osm)


## Downloading modules ##

Install osm using pip:
```bash
pip3 install --user -U https://github.com/Pbarbecho/osm/archive/master.zip
```

Depending on the operating system, you may need to add ~/.local/bin to your path. The pip will warn you about this in the installation. In case of user want to uninstall osm: 

```bash
pip3 uninstall osm
```


## Clone the source repository from Github ##
First, we recommend to install osm on a virtual environment:
```bash
pip3 install pipenv
```

To clone and install the osm repository, on the command line, enter:
```bash
git clone https://github.com/Pbarbecho/osm.git
```

Then, for use the new virtual environment instantiate a sub-shell as follows:

```bash
pipenv shell
```

On the new venv, install osm:

```bash
pipenv install osm/
```

At this time, you can interact with the osm modules, customize you analysis and use osm utilities. 

## Authors ##

Pablo Barbecho

[rtd]: https://osm.readthedocs.io/en/latest/
