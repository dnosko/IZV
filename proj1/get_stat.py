#%%
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np

def plot_stat(data_source, fig_location = None, show_figure = False):
    
    #print(data_source[0]) stĺpce
    region = data_source[1][0]
    date = data_source[1][4]
    
    # count occurances for each region
    regions = [] #list of regions in dataset
    i = 0
    dic_years = {}
    while i < len(region):
        count = np. count_nonzero(region==region[i]) + i
        regions.append(region[i])
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

    #sort arrays descending toto netreba :))) iba priradit cisla nad grafy podla poradia
    for year in dic_years.keys():
        dic_years[year] = sorted(dic_years[year], key=lambda x: x[1],reverse=True)
    
    fig, axes = plt.subplots(ncols=3, nrows=2,constrained_layout=True,figsize=(10,4))
    #print_x = []
    #print_y = []
    header = []
    #get x and y lists for graphs
    for year in dic_years.keys():
        for ax in axes.reshape(-1):
            print_y = [y for (x, y) in dic_years[year]]
            print_x = [x for (x, y) in dic_years[year]]
            ax.bar(print_x, print_y, width=0.7, bottom=0, align='center',color='C3')
            continue
    
    
    #for ax in axes.reshape(-1):
    #    ax.bar(print_x[i], print_y[i], width=0.7, bottom=0, align='center',color='C3')
    #    i = i + 1
    
    plt.show()


if __name__ == "__main__":
    plot_stat(DataDownloader().get_list(['MSK','PHA']))
    