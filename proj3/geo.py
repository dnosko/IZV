#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily
import sklearn.cluster
import numpy as np
# muzeze pridat vlastni knihovny


def _set_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ Nastavenie kategorickych datovych typov a nastavenie datetime"""
    # change to datetime
    df = df.rename(columns={'p2a': 'date'})
    df['date'] = pd.to_datetime(df['date'])

    columns = list(df)
    del columns[-1]  # delete region
    #set types
    type_dic = {'p1': 'int32', 'p13a' :'int32','p13b' :'int32','p13c' :'int32',
                'p47': 'int32', 'p53':'int32', 'd':'float64','e':'float64',
                'f':'float64','g':'float64','h':'string','i':'string','k':'string'}
    df = df.astype(type_dic)

    for i in columns:
        if i not in type_dic and i != 'date':
            df[i] = df[i].astype("category")

    return df

def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    df = _set_dataframe(df)

    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]),
                                 crs="EPSG:5514")
    # odstran nezname pozicie
    gdf = gdf[gdf['geometry'].is_valid]

    return gdf

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """



if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    #plot_geo(gdf, "geo1.png", True)
    #plot_cluster(gdf, "geo2.png", True)

