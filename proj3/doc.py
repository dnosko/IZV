#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
from pandas.api.types import CategoricalDtype
import seaborn as sns
from matplotlib.patches import Patch
import numpy as np

def _set_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ Nastavenie kategorickych datovych typov a nastavenie datetime"""
    # change to datetime
    df = df.rename(columns={'p2a': 'date'})
    df['date'] = pd.to_datetime(df['date'])

    columns = list(df)
    del columns[-1]  # delete region
    # set types
    type_dic = {'p1': 'int32', 'p13a': 'int32', 'p13b': 'int32', 'p13c': 'int32',
                'p47': 'int32', 'p53': 'int32', 'd': 'float64', 'e': 'float64',
                'f': 'float64', 'g': 'float64', 'h': 'string', 'i': 'string', 'k': 'string'}
    df = df.astype(type_dic)

    for i in columns:
        if i not in type_dic and i != 'date':
            df[i] = df[i].astype("category")

    return df

def mold_table(cols, names, df: pd.DataFrame):
    """ Sets table to desired structure.
     """
    main_col = cols[0]
    people = df[cols]
    melted_table = people.melt(id_vars=main_col, var_name="types")
    table = pd.pivot_table(melted_table, columns="types", index=main_col, values="value", aggfunc=["sum", "count"])
    #  drop repeating columns
    table = table.drop(table.columns[[4, 5]], axis=1)
    #  rename last column to count
    table.columns = names
    #  sort table
    table = table.reindex(table.sort_values(by='count', ascending=False).index)

    table = table.reset_index()

    return table

def sort_to_bins(df: pd.DataFrame, labels, bins, col):
    """ Sort column to bins and labels the bins """
    df[col] = pd.cut(df[col], bins, labels=labels, right=False)
    return df

def plot_graph(df: pd.DataFrame) -> pd.DataFrame:
    #  sort data to bins
    accident_type = ['nezaviňená řidičem', 'nepřiměřená rychlost jízdy', 'nesprávné předjíždění',
                     'nedání přednosti v jízdě', 'nesprávný způsob jízdy', 'technická závada vozidla']

    df = sort_to_bins(df, accident_type, [100, 201, 301, 401, 501, 601, 616], 'p12')

    table = mold_table(['p12', 'p13a', 'p13b', 'p13c'],['Úmrtia', 'Ťažko zranení', 'Ľahko zranení', 'count'],df )

    plot(table)

    return table

def plot(df: pd.DataFrame):
    # plot 3 subplots

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    #  set graphs
    axis_y = df.columns[1:]
    i = 0

    colors = sns.color_palette('Reds_d', n_colors=len(df))

    # set axes
    for ax in axes:
        # set grid
        ax.yaxis.grid(True)
        # plot graph
        sns.barplot(x="p12", y=axis_y[i], data=df,
                    ax=ax, palette=colors)
        # remove x label
        x_axis = ax.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)
        # remove y label
        y_axis = ax.axes.get_yaxis()
        y_label = y_axis.get_label()
        y_label.set_visible(False)
        # set title
        ax.title.set_text(axis_y[i])
        #ax.legend().set_visible(False)

        ax.get_xaxis().set_visible(False)
        i = i + 1

    # setup the legend
    # map names to colors
    cmap = dict(zip(df.p12, colors))

    # create the rectangles for the legend
    patches = [Patch(color=v, label=k) for k, v in cmap.items()]

    # add the legend
    plt.legend(title='Príčina nehody', handles=patches, bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0,
               fontsize=8)

    fig.tight_layout()
    plt.savefig('fig.png')


def substances_deaths(df: pd.DataFrame):
    """ Most deaths by drivers under influence in average: """

    alcohol = ['alkohol do 0.24', 'triezvy', 'alkohol do 0.5','drogy','drogy a alkohol',
                     'alkohol do 1.0', 'alkohol do 1.5', 'alkohol viac ako 1.5']
    bins = [1, 2, 3, 4, 5, 7,8,9,10]
    df['p11'] = pd.cut(df['p11'], bins, labels=alcohol, right=False)

    accident_type = ['nezaviňená řidičem', 'nepřiměřená rychlost jízdy', 'nesprávné předjíždění',
                     'nedání přednosti v jízdě', 'nesprávný způsob jízdy', 'technická závada vozidla']

    df = sort_to_bins(df, accident_type, [100, 201, 301, 401, 501, 601, 616], 'p12')
    # aggregate counts
    table = df.p11.groupby([df.p12, df.p11]).count().unstack().fillna(0).astype(int)
    # set total
    table.columns = table.columns.add_categories(['Celkom'])
    table['Celkom'] = table.sum(axis=1)
    # transpose - switch cols and rows
    table = table.T
    # print table to output
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print('LATEX:')
        print(table.to_latex(index=True))

    print_substances('p13a',['Úmrtia','úmrtí'])
    print_substances('p13b', ['Tažké zranenia', 'zranení'])

def print_substances(col, text):
    table = df.groupby('p11')[col].agg(['sum', 'count', 'mean']).reset_index()
    table = table.sort_values(by='mean', ascending=False)
    print(table)
    print(text[0],"sú najčastejšie spôsobené vodičom pod vplyvom:")
    for i in range(3):
        print(table.iat[i, 0], ' priemerne:', "{:.3f}".format(table.iat[i, 3]), text[1])
    print(table.iat[-1, 0], ' priemerne:', "{:.3f}".format(table.iat[-1, 3]), text[1])


def print_values(graf: pd.DataFrame):
    graf = graf.rename(columns={'p12':'Príčina nehody'})
    graf = graf.set_index('Príčina nehody')
    print(graf)

if __name__ == "__main__":
    df = pd.read_pickle("accidents.pkl.gz", compression='gzip')
    df = _set_dataframe(df)
    #graf = plot_graph(df)
    #print_values(graf)
    substances_deaths(df)
    pass
