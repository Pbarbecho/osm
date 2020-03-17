import os


def project(project_path, ext, name):

    """

    """
    os.chdir(project_path)
    cmd = 'opp_makemake -e {1} -M release -f --deep -o {2}'.format(project_path, ext, name)
    os.system(cmd)
    #os.chdir(output_path)
    #os.system('make')


def compilale_scenario(max_processors, veins_ini_file):
    """ Clean and compile project """
    os.chdir(veins_ini_file + '/../..')
    os.system("make MODE=release -j{0} clean".format(max_processors))
    os.system("make MODE=release -j{0} all".format(max_processors))




