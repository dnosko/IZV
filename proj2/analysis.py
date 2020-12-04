#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
from pandas.api.types import CategoricalDtype
import seaborn as sns
import numpy as np


# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    df = pd.read_pickle(filename, compression='gzip')

    orig_size = df.memory_usage(deep=True)

    # change to datetime
    df = df.rename(columns={'p2a': 'date'})
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date

    columns = list(df)
    del columns[-1]  # delete region

    for i in columns:
        df[i] = df[i].astype("category")

    if verbose:
        MB = 1048576
        new_size = df.memory_usage(deep=True)
        print('orig_size={:.1f} MB'.format(orig_size.sum() / MB))
        print('new_size={:.1f} MB'.format(new_size.sum() / MB))

    return df


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    people = df[['region', 'p13a', 'p13b', 'p13c']]
    melted_table = people.melt(id_vars="region", var_name="types")
    table = pd.pivot_table(melted_table, columns="types", index="region", values="value", aggfunc=["sum", "count"])

    #  drop repeating columns
    table = table.drop(table.columns[[4, 5]], axis=1)
    #  rename last column to count
    table.columns = ['p13a', 'p13b', 'p13c', 'count']
    #  sort table
    table = table.reindex(table.sort_values(by='count', ascending=False).index)

    table = table.reset_index()

    fig, axes = plt.subplots(4, 1, figsize=(16, 16))

    #  set graphs
    titles = ['Úmrtia', 'Ťažko zranení', 'Ľahko zranení', 'Celkový počet nehôd']
    colors = ['tab:blue', 'tab:green', 'tab:red', 'tab:orange']
    axis_y = table.columns[1:]
    i = 0

    # set axes
    for ax in axes:
        # set grid
        ax.yaxis.grid(True)
        sns.barplot(x="region", y=axis_y[i], data=table,
                    ax=ax, color=colors[i])
        # remove x label
        x_axis = ax.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)
        # remove y label
        y_axis = ax.axes.get_yaxis()
        y_label = y_axis.get_label()
        y_label.set_visible(False)
        # set title
        ax.title.set_text(titles[i])
        # set background
        ax.set_facecolor('xkcd:black')
        i = i + 1

    fig.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    pass


# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    pass


if __name__ == "__main__":
    pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    # plot_damage(df, "02_priciny.png", True)
    # plot_surface(df, "03_stav.png", True)
