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
    # count occurances for each region
    i = 0
    dic_years = {}
    while i < len(region):
        count = np. count_nonzero(region==region[i]) + i
        #print(region[i],"count:",count-i)
        region_dates = date[i:count]
        #print('unsorted',region_dates)
        sorted_arr = np.sort(region_dates)
        #get years
        years = list(sorted(set([arr[:4] for arr in sorted_arr])))
        #count number of accidents in each year
        cnt_arr = np.zeros(len(sorted_arr))
        for year in years:
            year_cnt = [np.count_nonzero(a[:4]==year) for a in sorted_arr]
            cnt_arr = np.add(cnt_arr,year_cnt)
            print(year)
        print(cnt_arr)
        year_ind = 0
        region_dic = {}
        for year in years:
            if year not in dic_years:
                dic_years[year] = []
            dic_years[year].append((region[i],int(cnt_arr[year_ind])))
            year_ind = year_ind + 1
            
        i = count
    print(dic_years)
    #print(region)
    #print(date)

    x = np.linspace(0,20,100)
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(2,1,1)
    ax.plot(x1, y1)
    ax.plot(x2,y2)
    ax2 = fig.add_subplot(2,2,2)
    ax.plot(x3, y3)
    plt.show()



if __name__ == "__main__":
    plot_stat(DataDownloader().get_list(['PHA']))
    