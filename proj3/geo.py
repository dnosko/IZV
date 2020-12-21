#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
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

def _show_fig(fig_location: str = None, show_figure: bool = False):
    """ Saves figure to given location. If show_figure=True, shows figure. """
    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()

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

    # vyfiltruj iba jeden region - JHM
    gdf = gdf.loc[gdf['region'] == "JHM"]

    # prirad farby a popis k cislam: 1 v obci, 2 mimo obce
    attrib = {1:("v obci","tab:red"), 2:("mimo obce","tab:blue")}

    lims_y = []
    lims_x = []
    # nastav graf
    fig, axes = plt.subplots(1,2, figsize=(18,8))
    i = 0
    for ax in axes:
        val = list(attrib.keys())[i]
        color = attrib[val][1]
        title = "Nehody v JHM kraji: " + attrib[val][0]
        gdf[gdf["p5a"] == val].plot(ax=ax, markersize=3, color=color)
        ax.axis("off")
        # najdi min a max hodnoty v kazdom podgrafe
        ymin, ymax = ax.get_ylim()
        lims_y.append(ymin)
        lims_y.append(ymax)
        xmin, xmax = ax.get_xlim()
        lims_x.append(xmax)
        lims_x.append(xmin)

        ax.set_title(title)
        i = i+1

    ymax = max(lims_y)
    ymin = min(lims_y)
    xmax = max(lims_x)
    xmin = min(lims_x)
    for ax in axes:
        ax.set_ylim(ymin,ymax)
        ax.set_xlim(xmin, xmax)
        ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.Stamen.TonerLite,
                        alpha=0.9)

    fig.tight_layout()
    _show_fig(fig_location, show_figure)

def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """



if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    #plot_cluster(gdf, "geo2.png", True)

