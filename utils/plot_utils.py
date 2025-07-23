#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 13:06:55 2025

@author: Fynn H
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator#, AutoMinorLocator
#import matplotlib.patches as mpatches
#import matplotlib.dates as mdates
#from datetime import datetime
import windrose #from ... import WindroseAxes, plot_windrose

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


from utils.df_utils import DataFrameUtils
from utils.data_utils import data_utils
# Its probably better to call the data functions from here

class DustPlots:
    color1 = 'darkkhaki'
    color2 = 'khaki'
    
    df_instance = DataFrameUtils()
    data_inst = data_utils()
    
    @staticmethod
    def subplot_station_index(station_name, plot_dict, plot_nao_dict, plot_enso_dict, start_year, end_year):
        fig, axs = plt.subplots(3,1, sharex=True, figsize=(13,5))
        lists = (plot_dict.items())
        x_val, y_val = zip(*lists)
        facecolor = ['darkkhaki' if y > 0.4 else 'khaki' for y in y_val]#'palegoldenrod'
        abs_y = [abs(y) for y in y_val]
        face_alphas = [n / max(abs_y) for n in abs_y]
        color_with_alphas = list(zip(facecolor, face_alphas))
    
        axs[0].bar(x_val,np.asarray(y_val), width=0.8, 
                   color=color_with_alphas,edgecolor = 'brown',
                label="all observations", zorder = 0)
        axs[0].set_ylabel('Dust Events/ All Events')
        axs[0].hlines(y=0.4,xmin= str(start_year)+"_1", xmax=str(end_year)+"_12",
                      linestyle=":", color="grey")
        
    
        lists = (plot_nao_dict.items())
        x_val, y_val = zip(*lists)
        facecolors = ["b" if y > 0 else "r" for y in y_val]
        #If i use the same facecolor for both I see positive nao in enso plot
        axs[1].bar(x_val,np.asarray(y_val), width=0.8, color=facecolors,
                label="NAO", zorder = 0)
        axs[1].tick_params(axis='x', labelrotation = 90)
        axs[1].set_ylabel('NAO Index')
        
    
        lists = (plot_enso_dict.items())
        x_val, y_val = zip(*lists)
        facecolors = ["b" if y > 0 else "r" for y in y_val]
        axs[2].bar(x_val,np.asarray(y_val), width=0.8, color=facecolors,
                label="ONI ENSO", zorder = 0)
        axs[2].tick_params(axis='x', labelrotation = 90)
        axs[2].set_ylabel('ONI ENSO Index')
    
        labels = np.arange(start_year, end_year +1, 1)
    
        axs[0].set_title("winter months from {y1}-{y2},{station}".format(
            station = station_name,y1=start_year,y2=end_year))
        axs[2].xaxis.set_major_locator(MultipleLocator(12))
        axs[2].xaxis.set_minor_locator(MultipleLocator(1))
        locs = list(axs[2].get_xticks())
        axs[2].set_xticks(locs[1:-1])
        #axs[2].set_xticklabels(labels)
        axs[2].tick_params(axis='x', which="major", width=3, length = 6)
        for ax in axs:
            ax.legend()
        plt.show()
    @staticmethod
    def plot_dust_perc( dust_perc,station_id):  
        df_instance = DataFrameUtils()
        station_name = df_instance.read_station_file(station_id)["name"]
        print(station_name)
        fig, ax = plt.subplots(1,1, figsize=(13,5))
        #Plotting Dictionary
        lists = sorted(dust_perc.items())
        x_val, y_val = zip(*lists)
        
        facecolor = ['darkkhaki' if int(y) > 15 else 'khaki' for y in y_val]
        abs_y = [abs(y) for y in y_val]
        face_alphas = [n / max(abs_y) for n in abs_y]
        color_with_alphas = list(zip(facecolor, face_alphas))
        ax.bar(x_val,np.asarray(y_val), width=0.8, color=color_with_alphas,
                edgecolor='brown', label="all observations", zorder = 0)
        ax.tick_params(axis='x', labelrotation = 90)
        #ax.tick_params(direction='out', length=6, width=2, colors='r',
                   #grid_color='r', grid_alpha=0.5)
        #ax.plot(x, y)
    
        ax.set_ylabel("Dust Events/All Events [%]")
        ax.set_xlabel("Year [AD]")
        ax.set_title("Percentage of dust events per year: {station}".format(
            station = station_name))
        plt.tight_layout()
        plt.show()
    @staticmethod   
    def plot_seasonality(station_name, dust_seasonality):
        keys = dust_seasonality.keys()
        colors = {"spring":"lightgreen","summer":"orange","fall":"purple","winter":"c"}
        fig, ax = plt.subplots(1,1, figsize=(13,5))

        for key in keys:
            lists = list(dust_seasonality[key].items())
            x_val, y_val = zip(*lists)
            
            ax.scatter(x_val,y_val, label = key, color = colors[key])
            plt.legend()

        plt.title("Seasonality of dust activity: {station}".format(
            station = station_name))
        plt.xlabel("Year")
        ax.tick_params(axis='x', labelrotation = 90)
        plt.ylabel("Dust Events/All Events")
        plt.show()
    
    #@staticmethod 
    def plot_season_comparison(object,df, id1, id2, timeframe, season="winter"):
        #ToDo Check if timeframe is valid
        #Try ZeroDivisionError
        df_instance = object.df_instance
        data_inst = object.data_inst
        
        station1 = df_instance.read_station_file(id1)
        station2 = df_instance.read_station_file(id2)
        
        df1 = df[df.STATION == id1]
        df1 = df1.sort_values(by="year",kind="mergesort")
        df2 = df[df.STATION == id2]
        df2 = df2.sort_values(by="year",kind="mergesort")
        plot_dict1 = data_inst.load_realtive_dust_days_by_season(df1, timeframe)
        plot_dict2 = data_inst.load_realtive_dust_days_by_season(df2, timeframe)
        season1 = data_inst.order_by_season(plot_dict1)[season]
        season2 = data_inst.order_by_season(plot_dict2)[season]
        
        fig, ax = plt.subplots(1,1, figsize=(13,5))
        
        lists = list(season1.items())
        x_val, y_val = zip(*lists)
        ax.scatter(x_val,y_val, label = station1["name"], color = "b",zorder = 1)
        
        lists = list(season2.items())
        x_val, y_val2 = zip(*lists)
        ax.scatter(x_val,y_val2, label = station2["name"], color = "orange", zorder = 1)
        
        difference = []
        for i in range(len(y_val)):
            difference.append(y_val2[i] - y_val[i])
        
        ax.plot(difference, label = "Difference",color = "k", zorder = 2)
        ax.grid(True)
        #ax.hlines(0, xmin= min(x_val), xmax=max(x_val), color = "k")
        
        plt.title("Comparison of Dust Events in " + season)
        #plt.xlabel("Year")
        ax.tick_params(axis='x', labelrotation = 90)
        plt.ylabel("Dust Events/All Events")
        plt.legend()
        plt.show()
        
    def plot_event_type(object, station_id, df, path):
        
        df_instance = object.df_instance
        data_inst = object.data_inst
        
        #event_types = df_instance.cluster_mw1(df)
        #zero_events = dust_perc
        station_name = df_instance.read_station_file(station_id,path)["name"]

        dict_dust = data_inst.calc_relative_dust_days(df, station_id)
        station_data = df[df.STATION == station_id]
        all_events = data_utils.get_number_of_events(station_data)
        cluster = data_inst.cluster_yearly_mw1(station_data, station_id)

        dust_perc = data_utils.calc_relativity(all_events, cluster)
        
        fig, ax = plt.subplots(1,1, figsize=(12,5))
        #Plotting Dictionary
        lists = sorted(dust_perc.items())
        x_val, y_val2 = zip(*lists)

        facecolor = ['darkkhaki' if y > 15 else 'khaki' for y in y_val2]
        #abs_y = [abs(y) for y in y_val]
        #face_alphas = [n / max(abs_y) for n in abs_y]
        #color_with_alphas = list(zip(facecolor, face_alphas))
        ax.bar(x_val,np.asarray(y_val2), width=0.8, color=facecolor,
                edgecolor='brown', label="0x events", zorder = 1)

        lists = sorted(dict_dust.items())
        x_val, y_val = zip(*lists)
        ax.bar(x_val,np.asarray(y_val), width=0.8, color="darkorchid",
               edgecolor = "indigo", label="dust events", zorder = 0)
        ax.tick_params(axis='x', labelrotation = 90)
        #ax.tick_params(direction='out', length=6, width=2, colors='r',
                   #grid_color='r', grid_alpha=0.5)
        #ax.plot(x, y)
        for i,j in enumerate(x_val):
            not_zero = np.round(dict_dust[j] - dust_perc[j],2)
            if not_zero != 0.00:
                ax.annotate(not_zero, (x_val[i],int(x_val[i][3])+4))

        ax.set_ylabel("Dust Events/All Events [%]")
        #ax.set_xlabel("Year [AD]")
        #ax.set_title()
        print("Percentage of dust events per year: {station}".format(
            station = station_name))
        plt.legend()
        plt.tight_layout()
        plt.show()
        
    def scatter_correlation(object,df, id1, id2, timeframe, season="winter"):
        #ToDo Better cmap
        #calculate correlation and plot it
        df_instance = object.df_instance
        data_inst = object.data_inst
        #timeframe_str = list(map(str,timeframe))
        #result = df.loc[df.year.isin(timeframe_str)]
        
        fig,ax  = plt.subplots(figsize=(6,5))
        
        if id1 == "NAO":
            plot_dict1 = data_inst.load_climate_index(name="NAO",timeframe=timeframe)
            ax.set_xlabel("NAO")
        else:
            station1 = df_instance.read_station_file(id1)
            df1 = df[df.STATION == id1]
            df1 = df1.sort_values(by="year",kind="mergesort")
            plot_dict1 = data_inst.load_realtive_dust_days_by_season(df1, timeframe)
            ax.set_xlabel("Dust Events Proportion {station}".format(station=station1["name"]))
        
        station2 = df_instance.read_station_file(id2)
        
        df2 = df[df.STATION == id2]
        df2 = df2.sort_values(by="year",kind="mergesort")
        
        plot_dict2 = data_inst.load_realtive_dust_days_by_season(df2, timeframe)
        
        season1 = data_inst.order_by_season(plot_dict1)[season]
        season2 = data_inst.order_by_season(plot_dict2)[season]
        
        #cv = data_inst.calc_relative_dust_days(df1, id1)
        #bb = data_inst.calc_relative_dust_days(df2, id2)
        #ZeroDivisionError
        #data_inst.load_realtive_dust_days_by_season
        
        
        lists = (season1.items())
        x_val, y_val = zip(*lists)
        lists2 = (season2.items())
        x_val, y_val2 = zip(*lists2)
        colors = []#np.zeros(len(x_val),dtype=str)
        labels = []#np.zeros(len(x_val),dtype=str)
        colors_dict = {"8":"#8130CF","9":"#CF3230","0":"#7ECF30","1":"#30CDCF","2":"#59D7D9"}#,"2":"#30CDCF"
        labels_dict = {"8":"1980s","9":"1990s","0":"2000s","1":"2010s","2":"2020s"}
        for i,j in enumerate(x_val):
            decade = j[2]
            if decade == "8":
                decade = "9"
            colors.append(colors_dict[decade])
            labels.append(labels_dict[decade])
        #color_marker = [int(x[2]) for x in x_val]
        #return colors, labels
        
        ax.scatter(y_val, y_val2,c=colors)#sc = ,cmap="Set3",label=labels
        
        a,b = np.polyfit(y_val, y_val2, 1)
        poly = np.zeros(len(y_val))
        for i,j in enumerate(y_val):
            poly[i] = a*j+b
        poly_label = "{m}x + {b}".format(m=np.round(a,3),b=np.round(b,3))
        
        print(poly_label)
        ax.plot(y_val,poly,label="Correlation \n {poly}".format(poly=poly_label), color = "k")
        #Fix Me: add a x = y line
        #ax.plot(y_val,y_val,label="x = y",color="k", linestyle="dotted")
        
        handles, labels = plt.gca().get_legend_handles_labels()
        
        for i,j in labels_dict.items():
            point = Line2D([0],[0], label = j, color = colors_dict[i],marker="s",linestyle="")
            handles.extend([point])
        
        #ax.set_xticks([0,0.1,0.2,0.3,0.4,0.5])
        '''if season in ["summer","spring"]:
            ax.set_yticks([0,0.1,0.2,0.3,0.4])
            ax.set_ylim(top = 0.4)
        elif season in ["winter","fall"]:
            ax.set_yticks([0,0.05,0.1,0.15])
            ax.set_ylim(top = 0.2)'''
        ax.set_ylim(top = 0.15)
        
        ax.set_ylabel("Dust Events Proportion {station}".format(station=station2["name"]))
        plt.title("Correlation in {seasons}".format(seasons=season))
        plt.legend(handles=handles)
        #fig.colorbar(sc)
        plt.show()
        corr = np.corrcoef(y_val,y_val2)
        if corr[0,0] == 1:
            print("Pearson: " + str(np.round(corr[0,1],2)))
        else:
            print("Not One: " + str(corr))
        
    @staticmethod
    def plot_windrose_subplots(data, *, direction, var, color=None, **kwargs):
        """wrapper function to create subplots per axis"""
        ax = plt.gca()
        ax = windrose.WindroseAxes.from_ax(ax=ax)
        windrose.plot_windrose(direction_or_df=data[direction], var=data[var], ax=ax, **kwargs)


    def subplot_sns(object, station_data):
        # this creates the raw subplot structure with a subplot per value in month.
        wind_data = pd.DataFrame({"ws": station_data.wind_speed.astype(float).div(10),
                     "wd": station_data.wind_dir.astype(int),
                     "month": station_data.month.astype(int)})
        g = sns.FacetGrid(
            data=wind_data,
            # the column name for each level a subplot should be created
            col="month",
            # place a maximum of 3 plots per row
            col_wrap=3,
            subplot_kws={"projection": "windrose"},
            sharex=False,
            sharey=False,
            despine=False,
            height=3.5,
        )
        
        g.map_dataframe(
            object.plot_windrose_subplots,
            direction="wd",
            var="ws",
            normed=True,
            # manually set bins, so they match for each subplot
            bins=(0.1, 1, 3, 5, 8, 13),
            calm_limit=0.1,
            kind="bar",
        )
        
        # make the subplots easier to compare, by having the same y-axis range
        y_ticks = range(0, 17, 4)
        for ax in g.axes:
            ax.set_legend(
                title=r"$m \cdot s^{-1}$", bbox_to_anchor=(1.15, -0.1), loc="lower right"
            )
            ax.set_rgrids(y_ticks, y_ticks)
        
        # adjust the spacing between the subplots to have sufficient space between plots
        plt.subplots_adjust(wspace=-0.2)
        plt.show()
        
    def cartopy_windrose(object, df, station_id, dust = True, season = False):
        df_instance = object.df_instance
        station = df_instance.read_station_file(station_id)
        station_data = df[df.STATION == station_id]
        station_data = station_data.drop(station_data[station_data.wind_speed == 999.9].index)
        station_data = station_data.drop(station_data[station_data.wind_dir == 999].index)
        
        
        #ToDo: Not WS but change in WS when dust event
        
        station_lat, station_lon = (station["lat"],station["lon"])
        
        minlon, maxlon, minlat, maxlat = (station_lon-0.25, station_lon+0.15, station_lat -0.25, station_lat + 0.15)
        
        proj = ccrs.PlateCarree()
        fig = plt.figure(figsize=(13, 9))
        # Draw main ax on top of which we will add windroses
        main_ax = fig.add_subplot(1, 1, 1, projection=proj)
        main_ax.set_extent([minlon, maxlon, minlat, maxlat], crs=proj)
        main_ax.gridlines(draw_labels=True)
        #main_ax.coastlines()
        main_ax.scatter(station_lon, station_lat, color = "r")
        
        request = cimgt.OSM()
        main_ax.add_image(request, 12)
        
        wrax_station = inset_axes(
            main_ax,
            width=2.5,  # size in inches
            height=2.5,  # size in inches
            loc="upper right",  # center bbox at given position
            bbox_to_anchor=(station_lon, station_lat),  # position of the axe
            bbox_transform=main_ax.transData,  # use data coordinate (not axe coordinate)
            axes_class=windrose.WindroseAxes,  # specify the class of the axe
        )
        if dust == True:
            station_dust = station_data[station_data.dust_occ == 1]
            ws_dust = station_dust.wind_speed.to_numpy()
            wd_dust = station_dust.wind_dir.astype(int).to_numpy()
            wrax_station.bar(wd_dust,ws_dust, normed = True,bins=np.array([0,3,7,15,20]))
        else:
            ws = station_data.wind_speed.to_numpy()
            wd = station_data.wind_dir.astype(int).to_numpy()
            wrax_station.bar(wd,ws,normed = True,bins=np.array([0,3,7,15,20]))
        
        wrax_station.tick_params(labelbottom=False)
        #main_ax.indicate_inset_zoom(wrax_station, edgecolor = "black")
        wrax_station.set_legend(title=r"$m \cdot s^{-1}$")
        y_ticks = range(0,41,10)
        wrax_station.set_rgrids(y_ticks, y_ticks)
        main_ax.set_title(df_instance.read_station_file(station_id)["name"])
        plt.show()