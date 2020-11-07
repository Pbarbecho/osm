import os
import pandas as pd
import matplotlib.pyplot as plt
from osm.campaign import new_folder
from osm.default_summarizer import parse_if_number
import pivottablejs as pj
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick


def custom_filter_plots(input_csv_file, output_directory, custom_pivot_table):
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

    new_folder(output_directory)
    df = pd.read_csv(input_csv_file)

    if custom_pivot_table:
        pj.pivot_ui(df)
        cmd = 'firefox pivottablejs.html'
        os.system(cmd)
    else:
        # Rename columns for axis plotting # TO DO
        df = df.rename(columns={evaluate: evaluate})

        # cambio filas
        #df = df.rename(columns={'accidentDuration': 'Beacon_interval(s)', 'beaconInterval': 'Accident_duration'})

        # Examples of custom analyze functions
        #node_speed(df, output_directory)
        #packet_losses_new(df, output_directory)
        rx_time_distribution(df, output_directory)
        distance(df, output_directory)
        #node_counter(df, output_directory)
        # Print outputs
        print('\nFiles generated: ')
        [print(' {}) {}'.format(i, file)) for i, file in enumerate(os.listdir(output_directory))]


def node_counter(tmp, output_directory):

        name = 'nodes'
        filename = '{}.csv'.format(name)
        plotname = '{}.pdf'.format(name)

        tmp = tmp.sort_values(by=['repetition'])
        tmp.reset_index(inplace=True)
        #tmp.to_csv(os.path.join(output_directory, filename))

        # setup style
        sns.set(font_scale=1.3, rc={'text.usetex': True}, style="whitegrid",
                palette=sns.palplot(sns.color_palette('Paired')), color_codes=True)

        f, axes = plt.subplots(figsize=(6, 6), sharex=False)
        sns.despine(left=False, top=False, right=False)

        #tmp = tmp[tmp.repetition <= 20]
        #tmp.to_csv(os.path.join(output_directory, 'tmp.csv'))


        # Filter maximum distance reached
        fig = sns.pointplot(x=evaluate, y='CounterNodes', hue='scenario', ci=100, errwidth=0.5,
                            capsize=0.3, markers=["o", "^", "s"], data=tmp, ax=axes)
        handles, labels = axes.get_legend_handles_labels()
        axes.legend(handles=handles[0:], labels=labels[0:])
        # Modify axes settings
        fig.set(xlabel=r"Vehicles' transmission range [m]", ylabel=r'\% of warned nodes')

        axes.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

        ax2 = plt.axes([0.6, 0.4, .2, .2])
        fig1 = sns.pointplot(x=evaluate, y='CounterNodes', hue='scenario', ci=100, errwidth=0.7,
                            capsize=0.06, markers=["o", "^", "s"], legend=False, data=tmp, ax=ax2)
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        #ax2.set_title('zoom')
        ax2.set_ylim([.88, .90])

        ax2.set_xlim([0.5, 0.6])

        #plt.xlim(100*.01, 450*0.01)
        ax2.legend_.remove()
        #ax2.set_xticklabels('')
        #ax2.set_yticklabels('')
        fig1.set(xlabel='', ylabel='')
        plt.show()
        # Save plot to default output_directory
        plt.savefig(os.path.join(output_directory, plotname), bbox_inches="tight")


def rx_time_distribution(tmp, output_directory):

    name = 'rx_time'
    filename = '{}.csv'.format(name)
    plotname = '{}.pdf'.format(name)

    tmp = tmp.sort_values(by=['repetition'])
    tmp.reset_index(inplace=True)
    tmp.to_csv(os.path.join(output_directory, filename))

    a = tmp.groupby(['scenario']).mean().reset_index()
    print(a)
    # setup style
    #sns.set(font_scale=1.2, rc={'text.usetex': True}, style="whitegrid",
    sns.set(font_scale=1.2, style="whitegrid",
            palette=sns.palplot(sns.color_palette('Paired')), color_codes=True)

    f, axes = plt.subplots(1, 1, figsize=(6, 6), sharex=False, sharey=False)
    sns.despine(left=False, top=False, right=False)

    # Filter maximum distance reached
    fig = sns.swarmplot(x='scenario', y=tmp['MsgTime']/60,  data=tmp)

    # Modify axes settings
    fig.set(xlabel=r"Accident duration [min]", ylabel=r'Warning msg arrival time [min]')

    # Save plot to default output_directory
    plt.savefig(os.path.join(output_directory, plotname), bbox_inches="tight")


def distance(tmp, output_directory):
    name = 'distance'
    filename = '{}.csv'.format(name)
    plotname = '{}.pdf'.format(name)

    tmp = tmp.sort_values(by=['repetition'])
    tmp.reset_index(inplace=True)
    tmp.to_csv(os.path.join(output_directory, filename))

    a = tmp.groupby(['scenario']).mean().reset_index()
    print(a)
    # setup style
    #sns.set(font_scale=1.2, rc={'text.usetex': True}, style="whitegrid",
    sns.set(font_scale=1.2, style="whitegrid",
            palette=sns.palplot(sns.color_palette('Paired')), color_codes=True)

    f, axes = plt.subplots(1, 1, figsize=(6, 6), sharex=False, sharey=False)
    sns.despine(left=False, top=False, right=False)

    # Filter maximum distance reached
    fig = sns.pointplot(x='scenario', y='MaxDistance', errwidth=1,  data=tmp)

    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles=handles[0:], labels=labels[0:])
    # Modify axes settings
    fig.set(xlabel=r"Node's coverage range [m]", ylabel=r'Maximum distance [m]')

    # Save plot to default output_directory
    plt.savefig(os.path.join(output_directory, plotname), bbox_inches="tight")


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
    pl_df['tx'] = tmp_tx.groupby(['scenario', 'Beacon_interval(s)', 'Accident_duration', 'repetition'])['MsgId'].count()
    pl_df['rx'] = tmp_rx.groupby(['scenario', 'Beacon_interval(s)', 'Accident_duration', 'repetition'])['MsgId'].count()

    # Compute packet losses
    pl_df['%PL'] = (1 - (pl_df.rx / pl_df.tx)) * 100

    # Sort and save
    pl_df = pl_df.reset_index(level=list(range(pl_df.index.nlevels)))
    pl_df.to_csv(os.path.join(output_directory, '{}.csv'.format(filename)), header=True)
    # Create plot
    fig = sns.catplot(x='Accident_duration', y='%PL', sharey=False, sharex=False, kind='box',  hue='Beacon_interval(s)', col='scenario',
        legend = True, legend_out = True, data=pl_df)
    # Modify axes settings
    fig.despine(right=False, top=False)
    fig.set_axis_labels('Accident duration (s)', '% Packet losses')
    # Save plot to default output_directory
    plt.savefig(os.path.join(output_directory, filename), bbox_inches="tight")


def packet_losses_new(tmp, output_directory):
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
    pl_df['tx'] = tmp_tx.groupby(['scenario', 'Beacon_interval(s)', 'Accident_duration', 'repetition'])['MsgId'].count()
    pl_df['rx'] = tmp_rx.groupby(['scenario', 'Beacon_interval(s)', 'Accident_duration', 'repetition'])['MsgId'].count()

    # Compute packet losses
    pl_df['%PL'] = (1 - (pl_df.rx / pl_df.tx)) * 100

    # Sort and save
    pl_df = pl_df.reset_index(level=list(range(pl_df.index.nlevels)))

    pl_df = pl_df[pl_df['Beacon_interval(s)'] == 30]  # 1,30,90

    pl_df.to_csv(os.path.join(output_directory, '{}.csv'.format(filename)), header=True)


    # Create plot primera vesion paper
    #fig = sns.catplot(x='Accident_duration', y='%PL', sharey=False, sharex=False, kind='box',  hue='Beacon_interval(s)', col='scenario',
    #    legend = True, legend_out = True, data=pl_df)

    # setup style
    sns.set(font_scale=1.3, rc={'text.usetex': True}, style="whitegrid",
            palette=sns.palplot(sns.color_palette('Paired')), color_codes=True)

    f, axes = plt.subplots(1, 1, figsize=(6, 6), sharex=False, sharey=False)
    sns.despine(left=False, top=False, right=False)


    fig = sns.pointplot(x='Accident_duration', y='%PL', hue='scenario', errwidth=1, capsize=0.1, markers=["o", "^", "s"], data=pl_df)
    handles, labels = axes.get_legend_handles_labels()

    axes.legend(handles=handles[0:], labels=labels[0:])
    # Modify axes settings
    fig.set(xlabel=r'Accident duration [s]', ylabel=r'\%  packet losses')

    plt.tight_layout()
    f.tight_layout()

    # Save plot to default output_directory
    name = '{}.pdf'.format(filename)
    plt.savefig(os.path.join(output_directory, name), bbox_inches="tight")


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
    #df["Accident_duration"] = [row.strip('-') for row in df["Accident_duration"]]

    # try to convert to numeric

    #if type(parse_if_number(df["Accident_duration"])) == float:
    #    df["Accident_Duration"] = pd.to_numeric(df["Accident_duration"], errors='coerce')

    # Filter tx packets

    tmp = df[(df['Type'] == 'node') & (df['Speed'] != 0)]

    # Sort and save
    tmp_speed = pd.DataFrame()
    tmp_speed['Speed'] = tmp.groupby(['scenario', 'Accident_duration', 'Beacon_interval(s)', 'repetition', 'Type', 'tx/rx'])['Speed'].mean()
    tmp_speed = tmp_speed.reset_index(level=list(range(tmp_speed.index.nlevels)))
    tmp_speed.to_csv(os.path.join(output_directory, '{}.csv'.format(filename)), header=True)

    # Plot
    fig = sns.catplot(kind='box', sym='', x='Accident_duration', y='Speed', hue='Beacon_interval(s)', col='scenario',  legend=True,
                      legend_out=True, data=tmp_speed)
    fig.set_axis_labels('Accident duration (s)', 'Speed (m/s)')
    plt.savefig(os.path.join(output_directory, filename), bbox_inches="tight")


def plots_folder(new_directory):
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)


def packet_delay(tmp, output_directory):
    """

    Average packet delay depending on the number of hops

    Input:
        csv file with results summary
    Output:
        custom plot

    """
    # add analyzer folder for plots
    plots_folder(output_directory)
    filename = "packet_delay.pdf"
    dataframe = pd.read_csv(tmp)

    dataframe_vehicles = dataframe.sort_values(by='NumberofVehicles')
    dataframe_vehicles = dataframe_vehicles.groupby(['NumberofVehicles']).mean()

    num_vehicles = []
    dataframe_keys = []

    #Create dataframe for each number of vehicles in the simulation
    for i in range(len(dataframe_vehicles)):
        num = dataframe_vehicles.index.get_level_values(0).values[i]
        num_vehicles.append(num)
        dataframe_keys.append("dataframe" + str(num))
    dataframes = dict.fromkeys(dataframe_keys)

    fig, ax = plt.subplots()

    for i in range(len(dataframe_vehicles)):
        #Create a dataframe for each number of vehicles and work with received packets
        dataframes[dataframe_keys[i]] = dataframe.loc[(dataframe.NumberofVehicles == num_vehicles[i]) & (dataframe.TR == 'rx')].sort_values(by=['Hops'])
        #Calculate mean delay for each number of hops
        dataframes[dataframe_keys[i]] = dataframes[dataframe_keys[i]].groupby(['Hops']).mean()
        #Plot dataframe
        plt.plot(dataframes[dataframe_keys[i]].index.get_level_values(0), dataframes[dataframe_keys[i]].Delay, "-o", label=("Vehicles density [veh/km2]: " + str(round(num_vehicles[i]/3.5,1)))) 
    #Format plot
    plt.grid()
    plt.legend(loc="upper left")
    plt.xlabel("Number of hops", fontsize=12)
    plt.ylabel("Average packet delay (s)", fontsize=12)
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    #Save figure
    plt.savefig(os.path.join(output_directory, filename))


def warned_vehicles(tmp, output_directory):
    """

    Percentage of warned vehicles when accident occurs

    Input:
        csv file with results summary
    Output:
        custom plot

    """
    # add analyzer folder for plots
    plots_folder(output_directory)
    filename = "warned_vehicles.pdf"
    count = []

    dataframe = pd.read_csv(tmp)


    #Get elements to iterate
    dataframe_vehicles = dataframe.sort_values(by='NumberofVehicles')
    dataframe_vehicles = dataframe_vehicles.groupby(['NumberofVehicles']).mean()
    num_vehicles = []

    #Get array with simulated number of vehicles
    for i in range(len(dataframe_vehicles)):
        num = dataframe_vehicles.index.get_level_values(0).values[i]
        num_vehicles.append(num)

    #Work only with received packets
    dataframe = dataframe.loc[dataframe.TR == 'rx']
    #Group to avoid vehicle repetition
    dataframe = dataframe.groupby(['NumberofVehicles', 'repetition', 'NodeID']).mean()

    for i in num_vehicles:
        for j in range(dataframe.index.get_level_values(1).nunique()):
            #Calculate percentage of vehicles that receive warning message
            count.append((len(dataframe.loc[(dataframe.index.get_level_values(0) == i) & (dataframe.index.get_level_values(1) == j)])*100)/i)

    #Group vehicles per number of vehicles and repetition
    dataframe = dataframe.groupby([dataframe.index.get_level_values(0), dataframe.index.get_level_values(1)]).mean()
    #Add percentage of warned vehicles to dataframe
    dataframe['Count'] = count

    #Prepare dataframe to plot
    data_plot = {"DensityofVehicles": np.round(dataframe.index.get_level_values(0)/3.5, 1), "Count": count}
    dataframe_plot = pd.DataFrame(data_plot, columns = ["DensityofVehicles", "Count"])

    #Plot dataframe
    fig, ax = plt.subplots()
    fig = sns.pointplot(x='DensityofVehicles', y='Count', data=dataframe_plot, join=False)
    #Format plot
    fig.set(xlabel='Density of vehicles [veh/km2]', ylabel='%  warned vehicles')
    plt.savefig(os.path.join(output_directory, filename))    


def warning_depth(tmp, output_directory):
    """

    Depth of the warning message (maximum distance it reaches from the accident) when accident occurs

    Input:
        csv file with results summary
    Output:
        custom plot

    """
    # add analyzer folder for plots
    plots_folder(output_directory)
    filename = "warning_depth.pdf"

    dataframe = pd.read_csv(tmp)

    #Work with rx packets and group by number of vechicles and repetition calculating maximum distance
    dataframe = dataframe.loc[dataframe.TR == 'rx']
    dataframe = dataframe.groupby(['NumberofVehicles', 'repetition']).max()

    #Prepare dataframe to plot
    data_plot = {"DensityofVehicles": np.round(dataframe.index.get_level_values(0)/3.5, 1), "WarningDepth": dataframe['DistanceToAccident']}
    dataframe_plot = pd.DataFrame(data_plot, columns = ["DensityofVehicles", "WarningDepth"])

    #Plot dataframe
    fig, ax = plt.subplots()
    fig = sns.pointplot(x='DensityofVehicles', y='WarningDepth', data=dataframe_plot, join=False)
    #Format plot
    fig.set(xlabel='Density of vehicles[veh/km2]', ylabel='Warning Depth (euclidian distance) [m]')
    plt.savefig(os.path.join(output_directory, filename))


def warning_depth_map(tmp, output_directory):
    """

    Depth of the warning message (maximum distance on the map it reaches from the accident) when accident occurs

    Input:
        csv file with results summary
    Output:
        custom plot

    """
    # add analyzer folder for plots
    plots_folder(output_directory)
    filename = "warning_depth_map.pdf"

    dataframe = pd.read_csv(tmp)

    #Work with rx packets and group by number of vechicles and repetition calculating maximum distance
    dataframe = dataframe.loc[dataframe.TR == 'rx']
    dataframe = dataframe.groupby(['NumberofVehicles', 'repetition']).max()

    #Prepare dataframe to plot
    data_plot = {"DensityofVehicles": np.round(dataframe.index.get_level_values(0)/3.5, 1), "WarningDepthMap": dataframe['SumoDistance']}
    dataframe_plot = pd.DataFrame(data_plot, columns = ["DensityofVehicles", "WarningDepthMap"])

    #Plot dataframe
    fig, ax = plt.subplots()
    fig = sns.pointplot(x='DensityofVehicles', y='WarningDepthMap', data=dataframe_plot, join=False)
    #Format plot
    fig.set(xlabel='Density of vehicles[veh/km2]', ylabel='Warning Depth (map distance) [m]')
    plt.savefig(os.path.join(output_directory, filename))