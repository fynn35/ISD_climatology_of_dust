#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 17:12:31 2025

@author: tow_lin
"""
#%% Imports
import numpy as np
import pandas as pd
import os
import seaborn as sns 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from datetime import datetime
import windrose

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from utils.df_utils import DataFrameUtils
from utils.data_utils import data_utils
from utils.plot_utils import DustPlots

df_instance = DataFrameUtils()
plot_instance = DustPlots()
data_inst = data_utils()

#%% Initiialize
path = os.path.dirname(__file__)[:-14]
dirname = path +"/ISD_data/"
fig_dir = path + "/figures/last_meeting"
file = "BBandCV"

df = pd.read_csv(dirname+file, na_values=9999, low_memory=False)

df2 = df_instance.load_ISD(df)
df2.STATION.loc[df2["STATION"] == 78954099999] = 78954000408

#%% Figure 1 Event type
# include BB event type
#make table
id1 = 8594099999
id2 = 78954000408
stations = [id1,id2]

path = dirname + "ISD_history.txt"

fig, axs = plt.subplots(2,1,sharex = True, figsize=(13,5))
table = {}
#Plotting Dictionary
for j,i in enumerate(stations):
    ax = axs[j]
    station_name = df_instance.read_station_file(i,path)["name"]

    
    station_data = df2[df2.STATION == i]
    station_data = station_data.sort_values(by="year",kind="mergesort")
    
    if j == 1:
        
        #station_data = station_data.drop(station_data[station_data.year.astype(int) <= 1950].index)
        station_data = station_data.drop(station_data[station_data.year == "1943"].index)
        station_data = station_data.drop(station_data[station_data.year == "1944"].index)
        station_data = station_data.drop(station_data[station_data.year == "1945"].index)
        station_data = station_data.drop(station_data[station_data.year == "1946"].index)
        '''station_data = station_data.drop[station_data.year == 1943]
        station_data = station_data.drop[station_data.year == 1944]
        station_data = station_data.drop[station_data.year == 1945]
        station_data = station_data.drop[station_data.year == 1946]'''
    all_events = data_utils.get_number_of_events(station_data)
    dict_dust = data_inst.calc_relative_dust_days(station_data, i)
    cluster = data_inst.cluster_yearly_mw1(station_data, i)

    dust_perc = data_utils.calc_relativity(all_events, cluster)
    lists = sorted(dust_perc.items())
    x_val, y_val2 = zip(*lists)
    
    facecolor = ['darkkhaki' if y > 10 else 'khaki' for y in y_val2]
    ax.bar(x_val,np.asarray(y_val2), width=0.8, color=facecolor,
            edgecolor='brown', label="blowing dust", zorder = 1)
    
    lists = sorted(dict_dust.items())
    x_val, y_val = zip(*lists)
    #if j == 1:
        #x_val = x_val[4:]
        #y_val = y_val[4:]
    ax.bar(x_val,np.asarray(y_val), width=0.8, color="k",
           edgecolor = "k", label="dust storms", zorder = 0)
    
    for n,m in enumerate(x_val):
        not_zero = np.round(dict_dust[m] - dust_perc[m],2)
        #Maybe just also put the year in
        #Or create a table
        
        if not_zero != 0.00:
            m = int(m)
            if m in table.keys():
                table[m] = table[m] + "&" + str(not_zero) + "\\\\"
            elif m not in table.keys():
                if j == 0:
                    table[m] = "&" + str(not_zero)
                else:
                    table[m] = "&    & " + str(not_zero) + "\\\\"
            
            #print(m + ": " + str(not_zero))
            #ax.annotate(not_zero, (x_val[i],int(x_val[i][3])+4))
    
    ax.set_ylabel("Dust Events/All Events [%]")
    print("Percentage of dust events per year: {station}".format(
        station = station_name))
    ax.annotate(str(j+1) + ")" , ("1949" ,np.max(y_val)-2) )
    ax.legend()

axs[1].tick_params(axis='x', labelrotation = 90)
#axs[0].annotate(str(1) + ")" , (x_val[0],0.41) )
#axs[1].annotate(str(2) + ")" , (x_val[0],0.31) )
for ax in axs:
    ax.set_xlim([0,66])
plt.tight_layout()
plt.show()
#%% Table 
test = dict(sorted(table.items()))
for key, value in test.items():
    if len(value) <= 6:
        value = value + "&   \\\\"
    print(str(key) + value)

#%% Figure 2 Seasonality
stations = [8594099999, 78954000408]
#stations = [8589099999]
start = 1980
end = 2020
timeframe = np.arange(start, end)
fig, axs = plt.subplots(2,1, sharex = True, figsize=(13,5))

for i,station_id in enumerate(stations):
    station_name = df_instance.read_station_file(station_id)["name"]
    station_df = df2[df2.STATION == station_id]
    station_df = station_df.sort_values(by="year",kind="mergesort")
    plot_dict = data_inst.load_realtive_dust_days_by_season(station_df, timeframe)
    dust_seasonality = data_inst.order_by_season(plot_dict)
    
    keys = dust_seasonality.keys()
    colors = {"spring":"#7ECF30","summer":"#CF3230","fall":"#8130CF","winter":"#30CDCF"}
    
    axs[i].set_axisbelow(True)
    axs[i].grid(color = "k", alpha = 0.5, zorder = 0)
    for key in keys:
        lists = list(dust_seasonality[key].items())
        x_val, y_val = zip(*lists)
        
        axs[i].scatter(x_val,y_val, label = key, color = colors[key], alpha=0.8)
        
    
    axs[i].set_ylabel("Dust Events/All Events")
    axs[i].legend()
    
axs[0].annotate(str(1) + ")" , (x_val[0],0.41) )
axs[1].annotate(str(2) + ")" , (x_val[0],0.31) )
axs[1].tick_params(axis='x', labelrotation = 90)
for ax in axs:
    ax.set_xlim([-1,40])
plt.tight_layout()
#plt.savefig(fig_dir + "seasonality.svg")
plt.show()

#%% Figure 3 Scatter Plot
start = 1980
end = 2020
timeframe = np.arange(start, end)
id2 = 78954000408
id1 = 8594099999 # independent variable : CV
seasons = ["spring","summer","fall"]#"winter",
fig,ax  = plt.subplots(1,3,sharey = True, sharex = True, figsize=(13,4))

for i, season in enumerate(seasons):
    
    station1 = df_instance.read_station_file(id1)
    df1 = df2[df2.STATION == id1]
    df1 = df1.sort_values(by="year",kind="mergesort")
    plot_dict1 = data_inst.load_realtive_dust_days_by_season(df1, timeframe)
    
    
    station2 = df_instance.read_station_file(id2)
    
    df3 = df2[df2.STATION == id2]
    df3 = df2.sort_values(by="year",kind="mergesort")
    
    plot_dict2 = data_inst.load_realtive_dust_days_by_season(df3, timeframe)
    
    season1 = data_inst.order_by_season(plot_dict1)[season]
    season2 = data_inst.order_by_season(plot_dict2)[season]
 
    lists = (season1.items())
    x_val, y_val = zip(*lists)
    lists2 = (season2.items())
    x_val, y_val2 = zip(*lists2)
    colors = []#np.zeros(len(x_val),dtype=str)
    labels = []#np.zeros(len(x_val),dtype=str)
    colors_dict = {"8":"#8130CF","9":"#CF3230","0":"#7ECF30","1":"#30CDCF","2":"#59D7D9"}#,"2":"#30CDCF"
    labels_dict = {"8":"1980s","9":"1990s","0":"2000s","1":"2010-2020"}
    for x,j in enumerate(x_val):
        decade = j[2]
        if decade == "2":
            decade = "1"
        colors.append(colors_dict[decade])
        labels.append(labels_dict[decade])
    
    ax[i].scatter(y_val, y_val2,c=colors)
    
    a,b = np.polyfit(y_val, y_val2, 1)
    poly = np.zeros(len(y_val))
    for n,m in enumerate(y_val):
        poly[n] = a*m+b
    poly_label = "{m}x + {b}".format(m=np.round(a,3),b=np.round(b,3))
    
    print(poly_label)
    ax[i].plot(y_val,poly,label="Correlation \n {poly}".format(poly=poly_label), color = "k")
    
    handles, labels = ax[i].get_legend_handles_labels()
    
    for ii,j in labels_dict.items():
        point = Line2D([0],[0], label = j, color = colors_dict[ii],marker="s",linestyle="")
        handles.extend([point])

    ax[i].legend(handles=handles)
    corr = np.corrcoef(y_val,y_val2)
    if corr[0,0] == 1:
        print("Pearson: " + str(np.round(corr[0,1],2)))
    else:
        print("Not One: " + str(corr))
    ax[i].annotate(str(i+1) + ")" , (np.min(y_val), np.max(y_val2)) )

ax[0].set_ylabel("Dust Events Proportion {station}".format(station=station2["name"]))
ax[1].set_xlabel("Dust Events Proportion {station}".format(station=station1["name"]))
plt.tight_layout()
plt.show()
#%% Figure 4 Scatter w/o 80s
start = 1995
end = 2024
timeframe = np.arange(start, end)
id2 = 78954000408
id1 = 8594099999 # independent variable : CV
seasons = ["spring","summer","fall"]#"winter",
fig,ax  = plt.subplots(1,3,sharey = True, sharex = True, figsize=(13,4))

for i, season in enumerate(seasons):
    
    station1 = df_instance.read_station_file(id1)
    df1 = df2[df2.STATION == id1]
    df1 = df1.sort_values(by="year",kind="mergesort")
    plot_dict1 = data_inst.load_realtive_dust_days_by_season(df1, timeframe)
    
    
    station2 = df_instance.read_station_file(id2)
    
    df3 = df2[df2.STATION == id2]
    df3 = df2.sort_values(by="year",kind="mergesort")
    
    plot_dict2 = data_inst.load_realtive_dust_days_by_season(df3, timeframe)
    
    season1 = data_inst.order_by_season(plot_dict1)[season]
    season2 = data_inst.order_by_season(plot_dict2)[season]
 
    lists = (season1.items())
    x_val, y_val = zip(*lists)
    lists2 = (season2.items())
    x_val, y_val2 = zip(*lists2)
    colors = []#np.zeros(len(x_val),dtype=str)
    labels = []#np.zeros(len(x_val),dtype=str)
    colors_dict = {"9":"#CF3230","0":"#7ECF30","1":"#30CDCF","2":"#8130CF"}#,"2":"#30CDCF"
    labels_dict = {"9":"1990s","0":"2000s","1":"2010s","2":"2020s"}
    for x,j in enumerate(x_val):
        decade = j[2]
        colors.append(colors_dict[decade])
        labels.append(labels_dict[decade])
    
    ax[i].scatter(y_val, y_val2,c=colors)
    
    a,b = np.polyfit(y_val, y_val2, 1)
    poly = np.zeros(len(y_val))
    for n,m in enumerate(y_val):
        poly[n] = a*m+b
    poly_label = "{m}x + {b}".format(m=np.round(a,3),b=np.round(b,3))
    
    print(poly_label)
    ax[i].plot(y_val,poly,label="Correlation \n {poly}".format(poly=poly_label), color = "k")
    
    handles, labels = ax[i].get_legend_handles_labels()
    
    for ii,j in labels_dict.items():
        point = Line2D([0],[0], label = j, color = colors_dict[ii],marker="s",linestyle="")
        handles.extend([point])

    ax[i].legend(handles=handles)
    corr = np.corrcoef(y_val,y_val2)
    if corr[0,0] == 1:
        print("Pearson: " + str(np.round(corr[0,1],2)))
    else:
        print("Not One: " + str(corr))
    ax[i].annotate(str(i+1) + ")" , (np.min(y_val), np.max(y_val2)) )

ax[0].set_ylabel("Dust Events Proportion {station}".format(station=station2["name"]))
ax[1].set_xlabel("Dust Events Proportion {station}".format(station=station1["name"]))
plt.tight_layout()
plt.show()

#%% Figure 5 Scatter NAO
start = 1995
end = 2024
timeframe = np.arange(start, end)
id2 = 8594099999 # CV
seasons = ["spring","summer","fall","winter"]
fig, axs  = plt.subplots(2,2,sharey = True, sharex = True, figsize=(9,9))

row = 0
for i, season in enumerate(seasons):

    col = i%2
    ax = axs[row][col]
    
    plot_dict1 = data_inst.load_climate_index(name="NAO",timeframe=timeframe)
    ax.set_xlabel("NAO")
    
    station2 = df_instance.read_station_file(id2)
    
    df3 = df2[df2.STATION == id2]
    df3 = df2.sort_values(by="year",kind="mergesort")
    
    plot_dict2 = data_inst.load_realtive_dust_days_by_season(df3, timeframe)
    
    season1 = data_inst.order_by_season(plot_dict1)[season]
    season2 = data_inst.order_by_season(plot_dict2)[season]
 
    lists = (season1.items())
    x_val, y_val = zip(*lists)
    lists2 = (season2.items())
    x_val, y_val2 = zip(*lists2)
    colors = []#np.zeros(len(x_val),dtype=str)
    labels = []#np.zeros(len(x_val),dtype=str)
    colors_dict = {"9":"#CF3230","0":"#7ECF30","1":"#30CDCF","2":"#8130CF"}#,"2":"#30CDCF"
    labels_dict = {"9":"1990s","0":"2000s","1":"2010s","2":"2020s"}
    for x,j in enumerate(x_val):
        decade = j[2]
        colors.append(colors_dict[decade])
        labels.append(labels_dict[decade])
    
    ax.scatter(y_val, y_val2,c=colors)
    
    a,b = np.polyfit(y_val, y_val2, 1)
    poly = np.zeros(len(y_val))
    for n,m in enumerate(y_val):
        poly[n] = a*m+b
    poly_label = "{m}x + {b}".format(m=np.round(a,3),b=np.round(b,3))
    
    print(poly_label)
    ax.plot(y_val,poly,label="Correlation \n {poly}".format(poly=poly_label), color = "k")
    
    handles, labels = ax.get_legend_handles_labels()
    
    for ii,j in labels_dict.items():
        point = Line2D([0],[0], label = j, color = colors_dict[ii],marker="s",linestyle="")
        handles.extend([point])

    ax.legend(handles=handles)
    corr = np.corrcoef(y_val,y_val2)
    if corr[0,0] == 1:
        print("Pearson: " + str(np.round(corr[0,1],2)))
    else:
        print("Not One: " + str(corr))
    ax.annotate(str(i+1) + ")" , (np.min(y_val), np.max(y_val2)) )
    if i == 1:
        row = 1

#ax[0].set_ylabel("Dust Events Proportion {station}".format(station=station2["name"]))
#ax[1].set_xlabel("Dust Events Proportion {station}".format(station=station1["name"]))
plt.tight_layout()
plt.show()
#%% Figure 6 Barbados Windrose
station_id = 78954000408
dust = False
seasons = ["spring","summer","fall", "winter"]

station = df_instance.read_station_file(station_id)
station_data = df2[df2.STATION == station_id]
station_data = station_data.drop(station_data[station_data.wind_speed == 999.9].index)
station_data = station_data.drop(station_data[station_data.wind_dir == 999].index)

station_lat, station_lon = (station["lat"],station["lon"])
station = df_instance.read_station_file(78954099999)
station_lat2, station_lon2 = (station["lat"],station["lon"])

minlon, maxlon, minlat, maxlat = (station_lon-0.5, station_lon+0.4, 
                                  station_lat -0.4, station_lat + 0.5)

query_dict = {"spring":"3 <= month <=5","summer":"6 <= month <=8", 
              "fall":"9 <= month <=11"}

proj = ccrs.PlateCarree()
fig = plt.figure(figsize=(13, 9))
# Draw main ax on top of which we will add windroses
main_ax = fig.add_subplot(1, 1, 1, projection=proj)
main_ax.set_extent([minlon, maxlon, minlat, maxlat], crs=proj)
main_ax.gridlines(draw_labels=True)
#main_ax.coastlines()
main_ax.scatter((station_lon2 ), (station_lat2), color = ("r"))

request = cimgt.OSM()
main_ax.add_image(request, 12)

loc_dict = {"spring":"lower right","summer":"lower left", 
              "fall":"upper right", "winter":"upper left"}
top = station_lat+0.1
bottom = station_lat -0.025
left = station_lon -0.135
right = station_lon + 0.05
bbox_dict = {"spring":(left, top),"summer":(right, top), 
              "fall":(left, bottom), "winter":(right, bottom)}
for i,season in enumerate(seasons):
    wrax_station = inset_axes(
        main_ax,
        width=2.5,  # size in inches
        height=2.5,  # size in inches
        loc=loc_dict[season],  # center bbox at given position
        bbox_to_anchor=bbox_dict[season],  # position of the axe
        bbox_transform=main_ax.transData,  # use data coordinate (not axe coordinate)
        axes_class=windrose.WindroseAxes,  # specify the class of the axe
    )
    if season == "winter":
        q1 = station_data.query("month <= 2")
        q2 = station_data.query("month == 12")
        test = pd.concat([q1,q2])
    else:
        test = station_data.query(query_dict[season])
    ws = test.wind_speed.to_numpy()
    wd = test.wind_dir.astype(int).to_numpy()
    
    wrax_station.bar(wd,ws,normed = True,bins=np.array([0,3,7,15,20]))
    wrax_station.tick_params(labelbottom=False)
    y_ticks = range(0,61,10)
    wrax_station.set_rgrids(y_ticks, [" ","10","20","30","40","50",""], angle = 315) 
    wrax_station.set_legend(title=r"$m \cdot s^{-1}$", loc = "lower left")
    wrax_station.set_title(season)
    

#main_ax.indicate_inset_zoom(wrax_station, edgecolor = "black")
#main_ax.set_title(df_instance.read_station_file(station_id)["name"])
plt.show()
#%% Table Atmosperic Correlation

id2 = 78954000408
id1 = 8594099999
start = 1980
end = 2021
timeframe = np.arange(start, end)
tmfr_leading = np.arange(start-1, end-1)
seasons = ["spring","summer","fall","winter"]
#df.STATION.loc[df["STATION"] == 78954099999] = 78954000408

df1 = df2[df2.STATION == id1]
df1 = df1.sort_values(by="year",kind="mergesort")
df3 = df2[df2.STATION == id2]
df3 = df3.sort_values(by="year",kind="mergesort")

# Correlation by season CV and BB
plot_dict1 = data_inst.load_realtive_dust_days_by_season(df1, timeframe)
plot_dict2 = data_inst.load_realtive_dust_days_by_season(df3, timeframe)

path = dirname
nao_dict = data_inst.load_climate_index(path,name="NAO",timeframe=timeframe)
enso_dict = data_inst.load_climate_index(path, name="ENSO",timeframe=timeframe)
enso_lead_dict = data_inst.load_climate_index(path, name="ENSO",timeframe=tmfr_leading)
print("Season & CV - BB & NAO - CV & ENSO - CV & Lead - CV & ENSO - BB \\\\")
for season in seasons:
    season1 = data_inst.order_by_season(plot_dict1)[season]
    lists = list(season1.items())
    x_val, y_cv = zip(*lists)
    season2 = data_inst.order_by_season(plot_dict2)[season]
    lists = list(season2.items())
    x_val, y_bb = zip(*lists)
    nao = data_inst.order_by_season(nao_dict)[season]
    lists = list(nao.items())
    x_val, y_nao = zip(*lists)
    enso = data_inst.order_by_season(enso_dict)[season]
    lists = list(enso.items())
    x_val, y_enso = zip(*lists)
    enso_lead = data_inst.order_by_season(enso_lead_dict)[season]
    lists = list(enso_lead.items())
    x_val, y_enso_lead = zip(*lists)
    
    #a,b = np.polyfit(y_val, y_val2, 1)
    #corr = np.correlate(y_val, y_val2)
    cv_bb = np.round(np.corrcoef(y_cv,y_bb)[0,1],2)
    nao_cv = np.round(np.corrcoef(y_nao,y_cv)[0,1],2)
    enso_cv = np.round(np.corrcoef(y_enso,y_cv)[0,1],2)
    enso_lead_cv = np.round(np.corrcoef(y_enso_lead,y_cv)[0,1],2)
    enso_bb = np.round(np.corrcoef(y_enso,y_bb)[0,1],2)
    #print(np.round(np.corrcoef(y_cv,y_nao)[0,1],2))


    print(season + "& "  + str(cv_bb)+ "& "  + str(nao_cv)
          + "& "  + str(enso_cv)+ "& "  + str(enso_lead_cv)
          + "& "  + str(enso_bb) + "\\\\")


#%% ? Praia Figure 1 Event type
station_id = 8589099999
path = dirname + "ISD_history.txt"

station_name = df_instance.read_station_file(station_id,path)["name"]

dict_dust = data_inst.calc_relative_dust_days(df2, station_id)
station_data = df2[df2.STATION == station_id]
all_events = data_utils.get_number_of_events(station_data)
cluster = data_inst.cluster_yearly_mw1(station_data, station_id)

dust_perc = data_utils.calc_relativity(all_events, cluster)

fig, ax = plt.subplots(1,1, figsize=(12,3))
#Plotting Dictionary
lists = sorted(dust_perc.items())
x_val, y_val2 = zip(*lists)

facecolor = ['darkkhaki' if y > 15 else 'khaki' for y in y_val2]
ax.bar(x_val,np.asarray(y_val2), width=0.8, color=facecolor,
        edgecolor='brown', label="0x events", zorder = 1)

lists = sorted(dict_dust.items())
x_val, y_val = zip(*lists)
ax.bar(x_val,np.asarray(y_val), width=0.8, color="darkorchid",
       edgecolor = "indigo", label="dust events", zorder = 0)
ax.tick_params(axis='x', labelrotation = 90)
for i,j in enumerate(x_val):
    not_zero = np.round(dict_dust[j] - dust_perc[j],2)
    #Maybe just also put the year in
    #Or create a table
    if not_zero != 0.00:
        print(j + ": " + str(not_zero))
        #ax.annotate(not_zero, (x_val[i],int(x_val[i][3])+4))

ax.set_ylabel("Dust Events/All Events [%]")
print("Percentage of dust events per year: {station}".format(
    station = station_name))
plt.legend()
plt.tight_layout()
plt.show()

#%% BB - CV
np.round(np.corrcoef(y_bb,y_cv)[0,1],2)
test = x_val[4:]


#%% Figure Overview Map
#for cartopy use stock image

#%% Figure Windrose CV
#use dust events and show that dust always comes from ~east
dust = True
#station_id = 8589099999
stations = [8594099999,8583099999,8594599999,8589099999,8594499999]

#def cartopy_windrose(df, station_id, dust = True):
    
minlon, maxlon, minlat, maxlat = (-25.5, -22.5, 14.7, 17.3)
proj = ccrs.PlateCarree()
fig = plt.figure(figsize=(13, 9))
# Draw main ax on top of which we will add windroses
main_ax = fig.add_subplot(1, 1, 1, projection=proj)
main_ax.set_extent([minlon, maxlon, minlat, maxlat], crs=proj)
main_ax.gridlines(draw_labels=True)
request = cimgt.OSM()
main_ax.add_image(request, 12)

locations = ["center right", "center left", "upper center", 
             "lower right", "center right"]
anchor = [(station_lon-0.25, station_lat), (station_lon + 0.25, station_lat),
          (station_lon, station_lat-0.5), (station_lon-0.05, station_lat+0.05),
          (station_lon-0.05, station_lat-0.2)]
def get_anchor(lon, lat, station):
    if station == 8594099999:
        return (station_lon-0.15, station_lat)
    elif station == 8583099999:
        return (station_lon + 0.25, station_lat)
    elif station == 8594599999:
        return (station_lon, station_lat-0.25)
    elif station == 8589099999:
        return (station_lon-0.15, station_lat+0.05)
    elif station == 8594499999:
        return (station_lon, station_lat-0.25)
    # I know that this is wrong but it works so piss off

for i, station_id in enumerate(stations):
    station = df_instance.read_station_file(station_id)
    station_data = df2[df2.STATION == station_id]
    station_data = station_data.drop(station_data[station_data.wind_speed == 999.9].index)
    station_data = station_data.drop(station_data[station_data.wind_dir == 999].index)
    
    station_dust = station_data[station_data.dust_occ == 1]
    #ToDo: Not WS but change in WS when dust event
    ws = station_data.wind_speed.to_numpy()
    wd = station_data.wind_dir.astype(int).to_numpy()
    
    ws_dust = station_dust.wind_speed.to_numpy()
    wd_dust = station_dust.wind_dir.astype(int).to_numpy()
    
    station_lat, station_lon = (station["lat"],station["lon"])

    main_ax.scatter(station_lon, station_lat, color = "r")

    

    wrax_station = inset_axes(
        main_ax,
        width=2,  # size in inches
        height=2,  # size in inches
        loc=locations[i],  # center bbox at given position
        bbox_to_anchor=get_anchor(station_lon, station_lat, station_id),  # position of the axe
        bbox_transform=main_ax.transData,  # use data coordinate (not axe coordinate)
        axes_class=windrose.WindroseAxes,  # specify the class of the axe
    )
    if dust == True:
        wrax_station.bar(wd_dust,ws_dust, normed = True,bins=np.array([0,3,7,15,20]))
    else:
        wrax_station.bar(wd,ws,normed = True,bins=np.array([0,3,7,15,20]))

    wrax_station.tick_params(labelbottom=False)
    wrax_station.set_title(station["name"].split("  ")[0])
#main_ax.indicate_inset_zoom(wrax_station, edgecolor = "black")
    #wrax_station.set_legend(title=r"$m \cdot s^{-1}$")
    y_ticks = range(0,61,10)
    wrax_station.set_rgrids(y_ticks, [" ","10","20","30","40","50",""], angle = 135)
#main_ax.set_title(df_instance.read_station_file(station_id)["name"])
plt.show()
#%% Figure Atmospheric Oscillations 
start = 1979
end = 2021
timeframe = np.arange(start, end)
plot_nao_dict = data_inst.load_climate_index(dirname,name="NAO",timeframe=timeframe)
plot_enso_dict = data_inst.load_climate_index(dirname, name="ENSO",timeframe=timeframe)

fig, axs = plt.subplots(2,1, sharex=True, figsize=(21,5))

lists = (plot_nao_dict.items())
x_val, y_val = zip(*lists)
facecolors = ["r" if y > 0 else "b" for y in y_val]
#If i use the same facecolor for both I see positive nao in enso plot
axs[0].bar(np.asarray(x_val), np.asarray(y_val), width=0.8, color=facecolors,
        label="NAO", zorder = 0)
axs[0].tick_params(axis='x', labelrotation = 90)
axs[0].set_ylabel('NAO Index')


lists = (plot_enso_dict.items())
x_val, y_val = zip(*lists)
facecolors = ["r" if y > 0 else "b" for y in y_val]
abs_y = [abs(y) for y in y_val]
face_alphas = [0.4 if n <= 0.5 else 1 for n in abs_y]
color_with_alphas = list(zip(facecolors, face_alphas))
axs[1].bar(np.asarray(x_val), np.asarray(y_val), width=0.8, color=color_with_alphas,
        label="ONI ENSO", zorder = 0)
axs[1].tick_params(axis='x', labelrotation = 90)
axs[1].set_ylabel('ONI ENSO Index')
axs[1].hlines(y=0.5,xmin= str(start)+"_1", xmax=str(end)+"_12",
              linestyle=":", color="k")
axs[1].hlines(y=-0.5,xmin= str(start)+"_1", xmax=str(end)+"_12",
              linestyle=":", color="k")

labels = np.arange(start, end+1 , 1)
major_ticks = np.arange(0,505,12)
minor_ticks = np.arange(2,505,3)

axs[0].set_xticks(major_ticks)
axs[0].set_xticks(minor_ticks, minor = True)

axs[1].set_xticklabels(labels)

for ax in axs:
    ax.grid(which="minor")
    ax.set_xlim([0,np.asarray(x_val).size])
plt.tight_layout()
plt.show()

#%% Figure Basemap

stations = list(df2.STATION.unique())
fifteen_north = {}

for station in stations:
    fifteen_north[station] = df_instance.read_station_file(station)
df = pd.DataFrame(fifteen_north)
lons = []
lats = []
label = []
country = {}
for i in df:
    lons.append(df[i]["lon"])
    lats.append(df[i]["lat"])
    label.append(i)
    country[df[i]["country"]] = [df[i]["lon"], df[i]["lat"]]

m = Basemap(projection = "merc",llcrnrlat=-0, urcrnrlat=30,\
            llcrnrlon=-75,urcrnrlon=0,lat_ts=20,resolution=None)
#width=12000000,height=9000000,projection='lcc',lat_1=0.,lat_2=30,lat_0=15,lon_0=-45.)
#m.drawcoastlines()
#m.drawlsmask()
#m.bluemarble()
m.etopo()
#m.shadedrelief()
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(0,31,15),labels=[1,1,0,0])
m.drawmeridians(np.arange(-75.,0,15.),labels=[0,0,0,1])
#m.drawmapboundary(fill_color='aqua') 

x,y = m(lons, lats)
m.scatter(x,y, marker='o',color='k')
for i in country:
    if i == "BB":
        x,y = m(country[i][0]+2, country[i][1]-3)
    elif i == "CV":
        x,y = m(country[i][0]+2, country[i][1]+1)
    plt.text(x,y,i,color='k')

#plt.title("ISD stations on Cape Verde and Barbedos")
plt.show()

#%% Station table
print("Station ID & Country & Location & Number of Entries \\\\")
for key, station in fifteen_north.items():
    name = station["name"].split("  ")[0] + "&"
    location = str(station["lat"]) + "\\textdegree N, " + \
                   str(station["lon"]*-1) + "\\textdegree W"
    print(str(key) + "&" + name + station["country"] + "&"+
          location + "&   \\\\")
#%%
for station in fifteen_north:
    station_size = df2[df2.STATION == station].size
    print(str(station) + ":" + str(station_size))
