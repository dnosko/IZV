#%%
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np

def plot_stat(data_source, fig_location = None, show_figure = False):
    
    #print(data_source[0]) stĺpce
    region = data_source[1][0]
    date = data_source[1][4]
    print('HERE')

    #potrebujem si podelit(slice) tu numpy array na zaklade poctu nazvu daneho kraja.
    #zoradit roky a spocitat
    
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
            print(year)
        print(cnt_lst)
        year_ind = 0
        for year in years:
            if year not in dic_years:
                dic_years[year] = []
            dic_years[year].append((region[i],cnt_lst[year_ind]))
            year_ind = year_ind + 1
            
        i = count

    #sort arrays descending
    for year in dic_years.keys():
        dic_years[year] = sorted(dic_years[year], key=lambda x: x[1],reverse=True)
    
    #fig, axes = plt.subplots(ncols=3, nrows=2,constrained_layout=True,figsize=(8,4))
    #(ax1,ax2,ax3),(ax4,ax5,ax6) = axes
    for year in dic_years.keys():
        yrs_val = [y for (x, y) in dic_years[year]]
        print('vals',yrs_val)
    #ax1.bar(regions, yrs_val, width=0.7, bottom=0, align='center',color='C3')
    #ax2.bar(regions, yrs_val, width=0.7, bottom=0, align='center',color='C3')
    #plt.show()


if __name__ == "__main__":
    plot_stat(DataDownloader().get_list(['MSK','PHA']))
    