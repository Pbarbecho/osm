import pandas as pd
import matplotlib.pyplot as plt
import os
from osm import campaign, merge
import pivottablejs as pj
import seaborn as sns


#sns.set(style="dark", color_codes=True)


def custom_filter_plots(input_csv_file, output_directory, custom_pivot_table, iter_parameters_path):
    """

    Here, user can edit/customize functions in order to analyze results.
    If interactive pivot table is true, an interactive (drag) panel containing
    the pivot table will appear inside a browser (Integrated with Jupyter).


    Inputs:
           Parse file containing all results from simulation campaign.
    Outputs:
           Custom filtered/sorted data files
           Customized plots (custom or using interactive pivot tables)


    """

    campaign.new_folder(output_directory)
    df = pd.read_csv(input_csv_file)

    if custom_pivot_table:
        pj.pivot_ui(df)
        cmd = 'firefox pivottablejs.html'
        os.system(cmd)
    else:
        iter_parameters = merge.get_iteration_parameters(iter_parameters_path)
        # Examples of custom analyze functions
        node_speed(df, output_directory)
        packet_losses(df, output_directory)

        # Print outputs
        print('\nFiles generated: ')
        [print(' {}) {}'.format(i, file)) for i, file in enumerate(os.listdir(output_directory))]


def packet_losses(tmp, output_directory):
    """

    Example of filtering/groping and computing percentage of packet Losses (%PL).

    Input:
        csv file containing parse file
    Output:
        csv file containing %PL
        custom bar plot

    """
    filename = 'summary_%PL_df'

    # filter input data frame
    tmp_tx = tmp[(tmp.Type == 'node') & (tmp['tx/rx'] == 'tx')]
    tmp_rx = tmp[(tmp.Type == 'rsu') & (tmp['tx/rx'] == 'rx')]

    # new dataframe for PL
    pl_df = pd.DataFrame()
    pl_df['tx'] = tmp_tx.groupby(['scenario', 'accidentDuration', 'beaconInterval', 'repetition'])['MsgId'].count()
    pl_df['rx'] = tmp_rx.groupby(['scenario', 'accidentDuration', 'beaconInterval', 'repetition'])['MsgId'].count()

    # Compute packet losses
    pl_df['%PL'] = (1 - (pl_df.rx / pl_df.tx)) * 100

    # Sort and save
    pl_df = pl_df.reset_index(level=list(range(pl_df.index.nlevels)))
    pl_df.to_csv(os.path.join(output_directory, '{}.csv'.format(filename)), header=True)

    # Plot
    fig = sns.catplot(x='beaconInterval', y='%PL', kind='box', sym='', hue='accidentDuration', col='scenario',
                      legend=True, legend_out=True, data=pl_df)
    fig.set_axis_labels('Beacon interval  (s)', '%  packet losses')
    plt.savefig(os.path.join(output_directory, filename), bbox_inches="tight")


def node_speed(df, output_directory):
    """

    Example of filtering nodes mean speed.

    Input:
        csv file containing parse file
    Output:
        csv file containing mean speed of all simulations in simulation campaign
        custom bar plot

    """
    filename = 'summary_speed'

    # strip - OMNET ++ syntax
    df["accidentDuration"] = [row.strip('-') for row in df["accidentDuration"]]

    # try to convert to numeric
    if type(merge.parse_if_number(df["accidentDuration"].iloc[0])) == float:
        df["accidentDuration"] = pd.to_numeric(df["accidentDuration"], errors='coerce')

    # Filter tx packets
    tmp = df[(df['Type'] == 'node') & (df['Speed'] != 0)]

    # Sort and save
    tmp_speed = pd.DataFrame()
    tmp_speed['Speed'] = tmp.groupby(['scenario', 'accidentDuration', 'beaconInterval', 'repetition', 'Type', 'tx/rx'])['Speed'].mean()
    tmp_speed = tmp_speed.reset_index(level=list(range(tmp_speed.index.nlevels)))
    tmp_speed.to_csv(os.path.join(output_directory, '{}.csv'.format(filename)), header=True)

    # Plot
    fig = sns.catplot(kind='box', sym='', x='accidentDuration', y='Speed', hue='beaconInterval', col='scenario',  legend=True,
                      legend_out=True, data=tmp_speed)
    fig.set_axis_labels('Accident duration  (s)', 'Speed (m/s)')
    plt.savefig(os.path.join(output_directory, filename), bbox_inches="tight")

"""
if __name__ == '__main__':

    df = pd.read_csv('/root/Documents/RESULTS/2hGAR/Dropbox/Python_Scripts/msmp/osm/summary/0xb42e99a4017b/results.csv')
    output_directory = '/root/Documents/RESULTS/2hGAR/Dropbox/Python_Scripts/msmp/osm/analyzer/0xb42e99a4017b/'
"""
