# -*- coding: utf-8 -*-
"""
Created on Fri May 30 2025

@author: Fynn H
"""


import numpy as np
import pandas as pd
import os
from utils.df_utils import DataFrameUtils
from utils.data_utils import data_utils
from utils.plot_utils import DustPlots

df_instance = DataFrameUtils()
plot_instance = DustPlots()
data_inst = data_utils()

#%% Get Directory Name
#dirname = '/media/tow_lin/E4A8-F53C/BA/ISD_data/'
dirname = os.path.dirname(__file__)[:-14]+"/ISD_data/"

#%% Import file
file = "4045431.csv" #BB
file = "3959221.csv" #CV
file = "BBandCV"

df = pd.read_csv(dirname+file, na_values=9999, low_memory=False)

df2 = df_instance.load_ISD(df)
df2.STATION.loc[df2["STATION"] == 78954099999] = 78954000408

start = 1995
end = 2024
timeframe = np.arange(start, end)
#%% Set variables

#What needs to be done to the df
station_id = 78954000408#8594099999
#station_id = 8594099999
#station_id = 78954099999
year = "1989"
station_name = df_instance.read_station_file(station_id)["name"]
nao_index = data_inst.load_climate_index(dirname ,name="NAO")
enso_index = data_inst.load_climate_index(dirname , name="ENSO")

#%% Plot the timeseries for that station
station_id = 8594499999
dust_rel = data_inst.calc_relative_dust_days(df2,station_id)
plot_instance.plot_dust_perc(dust_rel, station_id)

#%% Plot Event type
station_id = 8594099999#78954000408
path = dirname + "ISD_history.txt"
plot_instance.plot_event_type(station_id, df2, path)

#%% Set start and end year for a closer look



#%% Calculate and plot seasonalitiy of dust events
station_id = 8594099999
station_name = df_instance.read_station_file(station_id)["name"]
station_df = df2[df2.STATION == station_id]
station_df = station_df.sort_values(by="year",kind="mergesort")
plot_dict = data_inst.load_realtive_dust_days_by_season(station_df, timeframe)
dust_seasonality = data_inst.order_by_season(plot_dict)
plot_instance.plot_seasonality(station_name, dust_seasonality)

#%% Create a figure with dust events in a time frame and NAO and ENSO Index for
# that time frame
#ToDo: use seasonal dicts
path = dirname
plot_dict = data_inst.calc_relative_dust_days(df2,station_id, timeframe)

nao_dict = data_inst.load_climate_index(path,name="NAO",timeframe=timeframe)
enso_dict = data_inst.load_climate_index(path, name="ENSO",timeframe=timeframe)

plot_instance.subplot_station_index(station_name, plot_dict, nao_dict, enso_dict, start, end)

#%% Grantley Adams complete
id1 = 78954099999
id2 = 78954000408

station_data = df2[df2.STATION.isin([id1,id2])]
plot_dict = data_inst.calc_relative_dust_days(station_data)

plot_instance.plot_dust_perc(plot_dict, id1)

#%% season comparison
#id1 = 78954099999 
id1 = 78954000408
id2 = 8594099999

seasons = ["winter","spring","summer","fall"]
for i in seasons:
    plot_instance.plot_season_comparison(df2, id1, id2, timeframe,i)
#%% Scatter Plot 
id2 = 78954000408
id1 = 8594099999 # independent variable : CV
seasons = ["winter","spring","summer","fall"]
#y1, y2 = plot_instance.scatter_correlation(df2, id1, id2, timeframe, "summer")
for i in seasons:
    plot_instance.scatter_correlation(df2, id1, id2, timeframe, i)
#%% Scatter Plot Climate Index
id1 = "NAO"
id2 = 8594099999 # independent variable : CV
seasons = ["winter","spring","summer","fall"]
#y1, y2 = plot_instance.scatter_correlation(df2, id1, id2, timeframe, "summer")
for i in seasons:
    plot_instance.scatter_correlation(df2, id1, id2, timeframe, i)
#%% Station and climate indice in a season
path = dirname
station_id = 8594099999
station_name = df_instance.read_station_file(station_id)["name"]
season = "spring"
plot_dict = data_inst.calc_relative_dust_days(df2,station_id, timeframe)
season1 = data_inst.order_by_season(plot_dict)[season]

nao_dict = data_inst.load_climate_index(path,name="NAO",timeframe=timeframe)
nao_dict = data_inst.order_by_season(nao_dict)[season]
enso_dict = data_inst.load_climate_index(path, name="ENSO",timeframe=timeframe)
enso_dict = data_inst.order_by_season(enso_dict)[season]

plot_instance.subplot_station_index(station_name, season1, nao_dict, enso_dict, start, end)