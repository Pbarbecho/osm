import multiprocessing
import os
import subprocess
import uuid
import osm
import click


class Config(object):
    def __init__(self):
        self.verbose = False
        self.parents_dir = os.path.dirname(os.path.abspath('{}/..'.format(__file__)))
        self.mac = (hex(uuid.getnode()))  # mac to identify computer where simmualtions have been performed
        self.processors = multiprocessing.cpu_count()


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-v', is_flag=True, help=' verbose')
@pass_config
def cli(config, v):
    """

    CLI OSM Simulation manager. Execute large-scale OMNeT++ simulations.

    """
    config.verbose = v # verbose


###########
# Compile #
###########
@cli.command()
@click.argument('project-directory',
                type=click.Path(exists=True, resolve_path=True))
@click.option('-e', '--ext',
              help=' C++ source file extension, usually "cc" or "cpp".')
@click.option('-o', '--filename',
              help='Name of simulation executable to be built.'
                   'folder')
@pass_config
def build(config, project_directory, ext, filename):
    """

    Compile the project.

    """

    if ext not in ['cc', 'ccp']:
        ext = 'cc'
    osm.project(project_directory, ext, filename)


##########
# Launch #
##########
@cli.command()
@click.option('--omnet-path',
              type=click.Path(exists=True, resolve_path=True),
              help='OMNET++ installation directory')
@click.option('--output-dir',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to directory where results are saved.')
@click.option('--max-processes',
              default=1,
              help='The maximum number of parallel simulations. By default available cpus are used.')
@click.option('--sim-time', '-t',
              default=300,
              show_default=True,
              help='Simulation time. Common for all scenarios in simulation campaign.')
@click.option('-r', '--repetitions',
              default=1,
              show_default=True,
              help='Number of repetitions.')
@click.option('-a', '--analyze', is_flag=True,
              help='Analyze a group of files from a previous simulation campaign, looking for missing files.')
@click.option('-add', '--additional-files-path',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to iteration varibles and structure files. [default: parents directory]')
@click.option('--ned-file',  # path to .NED file
              type=click.Path(exists=True, resolve_path=True),
              help='path to .NED files')
@click.argument('inifile',  # path to veins ini file project
                type=click.Path(exists=True, resolve_path=True))
@click.argument('makefile',  # path to veins executable project
                type=click.Path(exists=True, resolve_path=True))
@pass_config
def launcher(config, omnet_path, output_dir, max_processes, sim_time, repetitions, analyze, additional_files_path,
             inifile,
             makefile, ned_file):
    """
    Build and run the simulation campaign

    Inputs: OMNET, VEINs installation paths. VEINs .ini file name and executable project name.
    Output: Simulation result per iteration in simulation campaign.

    """

    if config.verbose: click.echo('\n Setting program paths....')
    if additional_files_path is None:variables_path = os.path.join(config.parents_dir, 'variables')
    if output_dir is None: output_dir = os.path.join(config.parents_dir, 'results', config.mac)
    if omnet_path is None: omnet_path = get_omnetpp_installation_path('omnetpp')  # Try to get OMNeT++ installation
    if config.verbose:click.echo(omnet_path)

    # Try to get maximum number of processor and update setting
    updated_max_processes = get_MAX_PROCESS(config, max_processes)

    # Execute OMNET/VEINS simulation campaign
    osm.run(output_dir, updated_max_processes, omnet_path, sim_time, repetitions, analyze, variables_path, inifile,
            makefile, ned_file, config.verbose)


def get_MAX_PROCESS(config, max_processes):
    if max_processes == 1:
        # By default the max number of cpus are try to used in simulations
        max_processes = config.processors
    else:
        if config.processors < max_processes:
            max_processes = config.processors
    return max_processes


def get_omnetpp_installation_path(app):
    """
    If no path to OMNeT++ installation is pass. The script try to find OMNet++ installation path. In case of
    more than one OMNeT++ instance is found the first is chosen.

    Args:
        application: 'omnetpp'

    """

    command = 'whereis' if os.name != 'nt' else 'which'
    r = subprocess.getoutput('{0} {1}'.format(command, app))
    app_instance = (r.strip('omnetpp:').strip()).split(' ')
    if len(app_instance) > 1:
        click.echo('\n More than one OMNET installation found !!!')
        # TO DO menu to select OMNet++ instance
        return app_instance[0].strip('omnetpp')  # default first installation instance
    else:
        return app_instance.strip('omnetpp')


##########
# Parser #
##########
@cli.command()
@click.option('--max-processes',
              default=1,
              help='The maximum number of parallel simulations. By default available cpus are used.')
@click.option('-i', '--input-dir',
              type=click.Path(exists=True, resolve_path=True),
              help='Directory containing simulations results.')
@click.option('-o', '--output-dir',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to directory where output file is saved.')
@click.option('-O', '--output-filename',
              type=click.STRING,
              default="results.csv",
              show_default=False,
              help="Filename with supported extension .npy (Numpy), .mat (Matlab) or csv (Comma-separated values).")
@click.option('-add', '--additional-files-path',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to iteration varibles and structure files. [default: parents directory]')
@pass_config
def parser(config, max_processes, input_dir, output_dir, output_filename, additional_files_path):
    """
    Merge simulation campaign result files into one single output file.
    In case of OMNeT++ files are found in result files directory, OMNeT++ scavetool is used to generate .csv output file.

    Input: Results folder, iteration structure file (*not required in case of OMNeT results).
    Output: File extension Numpy .npy.

    """
    if output_dir is None: output_dir = os.path.join(config.parents_dir, 'summary', config.mac)
    if input_dir is None: input_dir = os.path.join(config.parents_dir, 'results', config.mac)
    if additional_files_path is None: additional_files_path = os.path.join(config.parents_dir)
    if os.path.exists(input_dir) and os.listdir(input_dir):
        updated_max_processes = get_MAX_PROCESS(config, max_processes)
        # Parser
        osm.merge_files(input_dir, output_dir, output_filename, additional_files_path, updated_max_processes)
    else:
        click.echo('No such file or directory or is empty: {}'.format(input_dir))


############
# Analyzer #
############
@cli.command()
@click.option('-i', '--input-cvs-file',
              type=click.Path(exists=True, resolve_path=True),
              help='Input .csv file with merge results')
@click.option('-o', '--output-dir',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to directory where custom analyzed factors are saved.')
@click.option('-plt', '--interactive-pivot-table', is_flag=True,
              help='GUI in firefox to drag columns and plot resutls dataframe.')
@pass_config
def analyzer(config, input_cvs_file, output_dir, interactive_pivot_table):
    """
    Custom Analyzer

    Input: Results folder, iteration structure file (*not required in case of OMNeT results).
    Output: File extension Numpy .npy.

    """

    if output_dir is None: output_dir = os.path.join(config.parents_dir, 'analyzer', config.mac)
    if input_cvs_file is None: input_cvs_file = os.path.join(config.parents_dir, 'summary', config.mac, 'results.csv')
    if os.path.exists(input_cvs_file):
        # Analyzer
        osm.custom_filter_plots(input_cvs_file, output_dir, interactive_pivot_table)
    else:
        click.echo('No such file or directory or is empty: {}'.format(input_cvs_file))
