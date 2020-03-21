<p align="center">
  <img src="doc/logo.png" width="400">
</p>

# Automating OMNeT++ simulations tool OVSM #

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


## Downloading modules ##

```bash
pip3 install --user -U https://github.com/Pbarbecho/osm/archive/master.zip
```

## Clone the source repository from Github ##

On the command line, enter:
```bash
git clone https://github.com/Pbarbecho/ovm.git
```

## Authors ##

Pablo Barbecho

[rtd]: https://simulationmanagerforomnet.readthedocs.io