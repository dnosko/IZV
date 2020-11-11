#%%
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np
import os, argparse

def plot_stat(data_source, fig_location=None, show_figure=False):

    region = data_source[1][0]
    date = data_source[1][4]
    
    # count occurrences for each region
    regions = set(region)  # set of regions in dataset
    i = 0
    dic_years = {}
    while i < len(region):
        count = np. count_nonzero(region == region[i]) + i
        # get dates from region only
        region_dates = date[i:count] 

        # extract years from date
        only_years = np.array([str(arr)[:4] for arr in region_dates])
        years = list(sorted(set(only_years)))
        # count number of accidents in each year
        cnt_lst = []
        for year in years:
            year_cnt = np.count_nonzero(only_years == year)
            cnt_lst.append(year_cnt)
        
        year_ind = 0
        for year in years:
            if year not in dic_years:
                dic_years[year] = []
            dic_years[year].append((region[i], cnt_lst[year_ind]))
            year_ind = year_ind + 1
            
        i = count

    # assign to positions of each region their order from highest to lowest (1,..,1+n)

    order = get_order(dic_years, len(regions))
    
    num_cols = int(len(dic_years) / 2) + 1
    
    fig, axes = plt.subplots(ncols=num_cols, nrows=2, constrained_layout=True, figsize=(8, 11))

    print_x = []
    print_y = []
    header = []
    # get x and y lists for graphs
    for year in dic_years.keys():
        header.append(year)
        print_y.append([y for (x, y) in dic_years[year]])
        print_x.append([x for (x, y) in dic_years[year]])

    # plot graphs
    plot_graph(axes, print_x, print_y, header, order)
    

    if fig_location:
        try:
            os.mkdir(fig_location)
        except FileExistsError:
            pass
        output_path = os.path.join(fig_location+'/graphs.png')
        plt.savefig(output_path)    
    

    if show_figure:
        plt.show(block=False)


def get_order(dic_years, len_seq):
    """ returns sequence of numbers. 1 is the region with highest rate. """

    order = []
    for year in dic_years.keys():
        a = [y for (x, y) in dic_years[year]]
        indexes = np.argsort(a)
        enum = [x for x in range(len_seq, 0, -1)]  # get reversed order
        try:
            for index in indexes:
                a[indexes[index]] = enum[index]
        except IndexError:
            pass

        order.append(a)

    return order


def plot_graph(axes, print_x, print_y, header, order):
    """ Function plots graph for each year in list header """
    
    i = 0
    for ax in axes.reshape(-1):
        try:
            y = print_y[i]
            x = print_x[i]
            bar = ax.bar(x, y, width=0.7, bottom=0, align='center', color='C3')
            ax.set_title(header[i])
            o = order[i]
            i = i + 1
            j = 0
            ax.tick_params(axis='x', labelrotation=90)
            for rect in bar: 
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., height,
                    '%d' % o[j],
                    ha='center', va='bottom')
                j = j + 1
        except IndexError:
            pass
    


def parse_args():
    """ Function parses arguments from command line """

    parser = argparse.ArgumentParser()

    parser.add_argument('--show_figure ', action='store_true', dest='show_fig')
    parser.add_argument('--fig_location', dest='fig_loc', type=str)

    args = parser.parse_args()
    return args.show_fig, args.fig_loc

if __name__ == "__main__":
    data_source = DataDownloader().get_list(['PHA', 'MSK', 'KVK'])
    args = parse_args()
    show_fig = args[0]
    fig_loc = args[1]
    plot_stat(data_source,fig_loc,show_fig)
    