#%%
from download import DataDownloader
import matplotlib.pyplot as plt
import numpy as np

def plot_stat(data_source, fig_location = None, show_figure = False):
    
    #print(data_source[0]) stĺpce
    region = data_source[1][0]
    date = data_source[1][4]

    #potrebujem si podelit(slice) tu numpy array na zaklade poctu nazvu daneho kraja.
    #zoradit roky a spocitat
    
    # count occurances for each region
    i = 0
    while i < len(region):
        count = np. count_nonzero(region==region[i]) + i
        print(region[i],"count:",count-i)
        if len(date[i:count]) == 0: #end of array
            region_dates = date[i:]
            print(region_dates)
            break
        else:
            region_dates = date[i:count]
            print(date[i:count])
        i = count
    print(region)
    print(date)

    x = np.linspace(0,20,100)
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(2,1,1)
    ax.plot(x1, y1)
    ax.plot(x2,y2)
    ax2 = fig.add_subplot(2,2,2)
    ax.plot(x3, y3)
    plt.show()



if __name__ == "__main__":
    plot_stat(DataDownloader().get_list(['PHA','PLK','ULK']))
    