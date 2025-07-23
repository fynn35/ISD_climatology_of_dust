#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 23:33:14 2025

@author: Fynn H 
"""

import pandas as pd
import numpy as np

class DataFrameUtils(object):#extends is not a python term#pd.DataFrame()
#

    @staticmethod
    def load_ISD(df, dirname="ISD_Data", file="temp.csv", save = False, current_year = "2025"):
        '''
        ToDo: seasons
        
        Parameters
        ----------
        df : pd.Dataframe
            Original ISD_Data
        dirname : str
            Directory where the .csv is saved.
        file : str
            name of the ISD file.
        save : Boolean, optional
            If the new df should be saved or just loaded. The default is False.
    
        Returns
        -------
        my_df : pd.Dataframe
            New df with all the needed variables for further analysis.
    
        '''
        #print("Hello World")
        
        #f = pd.DataFrame(df)
        
        if "WND" in df.keys():
            df[["wind_dir", "wind_dir_qc", "wind_type", "wind_speed", "wind_speed_qc"]]= df["WND"].str.split(",",expand=True)
        if "dust_occ" not in df.keys():
            df["dust_occ"] = np.where((df["MW1"] == "06,1") | (df["MW1"] == "07,1") |
                                      (df["MW1"] == "08,1") | (df["MW1"] == "09,1") |
                                      (df["MW1"] == "30,1") | (df["MW1"] == "31,1") |
                                      (df["MW1"] == "32,1") | (df["MW1"] == "33,1") |
                                      (df["MW1"] == "34,1") | (df["MW1"] == "35,1") |
                                      (df["MW1"] == "98,1") |
                                      (df["MW2"] == "06,1") | (df["MW2"] == "07,1") |
                                      (df["MW2"] == "08,1") | (df["MW2"] == "09,1") |
                                      (df["MW2"] == "30,1") | (df["MW2"] == "31,1") |
                                      (df["MW2"] == "32,1") | (df["MW2"] == "33,1") |
                                      (df["MW2"] == "34,1") | (df["MW2"] == "35,1") |
                                      (df["MW2"] == "98,1")
                                      , 1, 0)
        
        date_split = df.DATE.str.split("-",expand=True)
        df["year"] = date_split[0]
        df["month"] = date_split[1].astype(int)
        
        df = df.drop(df[df.year == current_year].index)
        
        df.wind_speed = df.wind_speed.astype(float).div(10)
        
        my_dict = {"STATION":df.STATION,"DATE":df.DATE , "year": df.year,
                   "month":df.month, "MW1":df.MW1,"MW2":df.MW2, "dust_occ":df.dust_occ, 
                   "WND":df.WND, "wind_dir":df.wind_dir, 
                   "wind_type":df.wind_type, "wind_speed":df.wind_speed}
        my_df = pd.DataFrame(my_dict)
        
        if save:
            my_df_name = dirname + "sm_" + file
            my_df.to_csv(my_df_name)
        return my_df
    @staticmethod
    def read_station_file(station_id,path="/media/tow_lin/E4A8-F53C/BA/ISD_data/ISD_history.txt"):
        '''
        Parse the station file to get metadata for the provided id

        Parameters
        ----------
        station_id : int
            DESCRIPTION.
        path : TYPE, optional
            DESCRIPTION. The default is "/media/tow_lin/E4A8-F53C/BA/ISD_data/ISD_history.txt".

        Returns
        -------
        station_info : Dict
            DESCRIPTION.

        '''
        #FixMe: See why split doesnt give results
        file = open(path)
        lines = file.readlines()[22:]
        for line in lines[:-1]:
    
             USAF = line[0:6]
             WBAN = line[7:12]
             name = line[13:42]
             #name = name.split("  ")
             ctry = line[43:45]
             lat_str = line[58:64]
             lon_str = line[66:73]
             height = line[74:81]
             if line[57] =="+":
                lat = float(lat_str)
             elif line[57] =="-":
                lat = - float(lat_str)
             if line[65] =="+":
                lon = float(lon_str)
             elif line[65]=="-":
                lon = - float(lon_str)
             
             try:
                station = int(USAF + WBAN)
                if station == station_id:
                   station_info = {"name":name,"lat": lat, "lon": lon, 
                                   "height": height, "country": ctry}
                   return station_info
                if type(station_id) == list:
                    for station in station_id:
                        station_info = {"name":name,"lat": lat, "lon": lon, 
                                        "height": height, "country": ctry}
                        stations_info = {station: station_info}
                        print(stations_info)
                        
                    return stations_info
             except ValueError:
                 continue
             file.close()
    
    
    
            
    @staticmethod
    def set_season(df):
        month = df.DATE.str.split("-", expand=True)[1]
        df["season"] = month
        return False