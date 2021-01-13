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

def plot_graph(df: pd.DataFrame) -> pd.DataFrame:
    #  sort data to bins
    accident_type = ['nezaviňená řidičem', 'nepřiměřená rychlost jízdy', 'nesprávné předjíždění',
                     'nedání přednosti v jízdě', 'nesprávný způsob jízdy', 'technická závada vozidla']
    bins = [100, 201, 301, 401, 501, 601, 616]
    df['p12'] = pd.cut(df['p12'], bins, labels=accident_type, right=False)

    people = df[['p12', 'p13a', 'p13b', 'p13c']]
    melted_table = people.melt(id_vars="p12", var_name="types")
    table = pd.pivot_table(melted_table, columns="types", index="p12", values="value", aggfunc=["sum", "count"])
    #  drop repeating columns
    table = table.drop(table.columns[[4, 5]], axis=1)
    #  rename last column to count
    table.columns = ['Úmrtia', 'Ťažko zranení', 'Ľahko zranení', 'count']
    #  sort table
    table = table.reindex(table.sort_values(by='count', ascending=False).index)

    table = table.reset_index()

    # plo
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

def print_values(graf: pd.DataFrame):
    graf = graf.rename(columns={'p12':'Príčina nehody'})
    graf = graf.set_index('Príčina nehody')
    print(graf)

if __name__ == "__main__":
    df = pd.read_pickle("accidents.pkl.gz", compression='gzip')
    df = _set_dataframe(df)
    graf = plot_graph(df)
    print_values(graf)
    pass
