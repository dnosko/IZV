#!/usr/bin/env python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
from pandas.api.types import CategoricalDtype
# import seaborn as sns
import numpy as np
import os
import gzip


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
    table = pd.pivot_table(melted_table, columns="types", index="region",values="value", aggfunc=np.sum)
    print(table)


    if fig_location:
        pass
        #plt.savefig(fig_location)

    if show_figure:
        pass
        #plt.show()


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
