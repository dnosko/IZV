#%%
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_stat(data_source, fig_location = None, show_figure = False):
    
    #print(data_source[0]) stĺpce
    region = data_source[1][0]
    date = data_source[1][4]
    
    # count occurances for each region
    regions = set(region) #set of regions in dataset
    i = 0
    dic_years = {}
    while i < len(region):
        count = np. count_nonzero(region==region[i]) + i
        #get dates from region only
        region_dates = date[i:count] 

        #extract years from date
        only_years = np.array([arr[:4] for arr in region_dates])
        years = list(sorted(set(only_years)))
        #count number of accidents in each year
        cnt_lst = []
        for year in years:
            year_cnt = np.count_nonzero(only_years==year)
            cnt_lst.append(year_cnt)
        
        year_ind = 0
        for year in years:
            if year not in dic_years:
                dic_years[year] = []
            dic_years[year].append((region[i],cnt_lst[year_ind]))
            year_ind = year_ind + 1
            
        i = count

    #assign to positions of each region, their order
    order = []
    for year in dic_years.keys():
        a = [y for (x, y) in dic_years[year]]
        indexes = np.argsort(a)
        print('indexes',indexes)
        print('values',a)
        enum = [x for x in range(4, 0,-1)] # get reversed order
        print('order',order)
        for index in indexes:
            a[indexes[index]] = enum[index]

        order.append(a)
    
    num_cols = int(len(regions) / 2) +1
    
    fig, axes = plt.subplots(ncols=num_cols, nrows=2,constrained_layout=True,figsize=(8,11))
    print_x = []
    print_y = []
    header = []
    #get x and y lists for graphs
    for year in dic_years.keys():
        header.append(year)
        print_y.append([y for (x, y) in dic_years[year]])
        print_x.append([x for (x, y) in dic_years[year]])
    

    #plot graphs
    plot_graph(axes,print_x,print_y,header,order)
    
    plt.tight_layout()
    

    if fig_location:
        output_path = os.path.join(fig_location+'/graphs.png')
        plt.savefig(output_path)    
    
    if show_figure:
        plt.show()


def plot_graph(axes,print_x,print_y,header,order):
    
    i = 0
    for ax in axes.reshape(-1):
        try:
            y = print_y[i]
            x = print_x[i]
            bar = ax.bar(x, y, width=0.7, bottom=0, align='center',color='C3')
            ax.set_title(header[i])
            
            j = 0
            for rect in bar: 
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., height,
                    '%d' % order[i][j],
                    ha='center', va='bottom')
                j = j + 1
            i = i + 1
        except IndexError:
            pass
    
    plt.tight_layout()



if __name__ == "__main__":
    plot_stat(DataDownloader().get_list(['MSK','PHA','OLK','PAK']),fig_location='data',show_figure=True)
    