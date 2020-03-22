import os
import uuid
import multiprocessing
import subprocess
import osm

if __name__ == '__main__':
    mac = hex(uuid.getnode())
    installation_path =  os.path.dirname(os.path.abspath('{}/..'.format(__file__)))
    results_folder = os.path.join(installation_path, 'results', mac)
    summary_results = os.path.join(installation_path, 'summary', mac)
    analyzer_folder = os.path.join(installation_path, 'analyzer', mac)
    processors = multiprocessing.cpu_count()

    command = 'whereis' if os.name != 'nt' else 'which'
    r = subprocess.getoutput('{0} {1}'.format(command, 'omnetpp'))
    app_instance = (r.strip('omnetpp:').strip()).split(' ')
    omnet_installation = app_instance[0].strip('omnetpp')  # default first installation instance
    omnet_ini_file = '/root/Documents/veins_example/veins/examples/veins/omnetpp.ini'
    project_exec = '/root/Documents/veins_example/veins/src/veins_example'

    osm.run(results_folder, processors, omnet_installation, 100, 2, False, installation_path, omnet_ini_file,
            project_exec, True)
    print('-'*50)
    osm.merge_files(results_folder, summary_results, 'output.csv', installation_path, processors)
    print('-' * 50)
    osm.custom_filter_plots(os.path.join(summary_results, 'output.csv'), analyzer_folder, False)

