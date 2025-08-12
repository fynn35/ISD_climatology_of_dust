#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 19:06:48 2025

@author: Fynn H
"""

import numpy as np
import pandas as pd

class data_utils():
    
    
    @staticmethod      
    def get_number_of_events(df):
        '''
        Method that returns a dictionary with the number of entries for each year from the passed dataframe
        
        Parameters
        ----------
        df : pd.Dataframe
            Dataframe of ISD measurements with multiple years of record

        Returns
        -------
        no_occur : Dictionary
            Dictionary containing integers. The key is the year. When df.year is a string the key is also a string
        '''
        years = df.year.unique()
        no_occur = {}
        for i in years:
            temp = df.drop(df[df.year != i].index)
            no_occur[i] = temp.year.size
        return no_occur
             
    @staticmethod    
    def calc_relative_dust_days(df, station_id=False, timeframe = None):
        '''
        Method that calculates the percentage of dust events against all measurements for the passed station.
    
        Parameters
        ----------
        df : pd.DataFrame
            Dataframe of ISD measurements
        station_id : int or list of int
            Default: False
            Unique station identifier.
        timeframe : list of strings
            Default: None
            If not all years in the dataframe are subject to analysis this list passes the years to analyse
            
        Returns
        -------
        dust_perc: Dictionary
            Relative number of dust days against all measurements
    
        '''  
        if type(station_id) == int:
            station_data = df[df.STATION == station_id]
        else:
            station_data = df
        dust = station_data.drop(station_data[station_data.dust_occ ==0].index)
                
        dust_events = data_utils.get_number_of_events(dust)
        all_events = data_utils.get_number_of_events(station_data)
    
        
        dust_perc = {}
        if type(timeframe) == np.ndarray:
            plot_dict = {}
            timeframe_str = list(map(str,timeframe))
            df_timeframe = station_data[station_data.year.isin(timeframe_str)]
            for year in df_timeframe.year.unique():
                for i in np.arange(1,13):
                    test = df_timeframe.loc[(df_timeframe.year == year) & (df_timeframe.month == i)]
                    dust = test.drop(test[test.dust_occ == 0].index)
                    if test.size != 0:
                        plot_dict[str(year) + "_" + str(i)] = dust.size/test.size
                    else:
                        plot_dict[str(year) + "_" + str(i)] = 0
            dust_perc = plot_dict
        else:
            
            for i in all_events:
                if i not in dust_events.keys():
                    dust_perc[i] = 0
                else:
                    dust_perc[i] = (dust_events[i]/all_events[i])*100
        
        return dust_perc
    
    @staticmethod 
    def calc_relativity(dict_1, dict_2):
        '''
        Calculate the percentage of events between two dictionaries for each key.

        Parameters
        ----------
        dict_1 : TYPE
            Dict with all events.
            eg. data_utils.get_number_of_events()
        dict_2 : TYPE
            Dict which should be set into relation with all events.
            eg. cluster_yearly_mw1()

        Returns
        -------
        dust_perc : Dictionary

        '''
        
        dust_perc = {}
        for i in dict_1:
            if i not in dict_2.keys():
                dust_perc[i] = 0
            else:
                dust_perc[i] = (dict_2[i]/dict_1[i])*100
        return dust_perc
                
    @staticmethod
    def load_climate_index(path="/ISD_data/",name=["NAO","ENSO"],timeframe = None):
        '''
        Load the monthly climate index from the file 

        Parameters
        ----------
        path : str
            Path to the file without file name
        name : str
            Choose a climate index between ["NAO","ENSO"]. This determines the file name
        timeframe : list of strings
            Default: None
            If not all years in the dataframe are subject to analysis this list passes the years to analyse

        Returns
        -------
        climate_index : dict
            Dictionary with monthly climate index. The key is the year_month as a string

        '''
        
        climate_index = {}
        if name == "NAO":
            file = open(path + "nao_pc_monthly.txt")
            lines = file.readlines()[1:]
            file.close()
            for line in lines[:-1]: #ignore current year
                year, jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec = \
                line.split()
                climate_index[year] = [jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec]
        elif name == "ENSO":
            file = open(path + "oni_monthly.txt")
            lines = file.readlines()[1:]
            file.close()
            for line in lines[:-9]: #ignore current year
                year, jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec = \
                line.split()
                climate_index[year] = [jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec]

        if type(timeframe) == np.ndarray:
            months_climate_dict = {}
            months_climate_dict[str(min(timeframe)-1)+"_"+"12"] = \
            float(climate_index[str(min(timeframe)-1)][11])
            for year in timeframe:
                temp = climate_index[str(year)]
                for i in np.arange(1,13):
                    if year == (max(timeframe)) and i == 12:
                        continue
                    else:
                        months_climate_dict[str(year) + "_" + str(i)] = float(temp[i-1])
            climate_index = months_climate_dict
        return climate_index
    
    @staticmethod
    def load_realtive_dust_days_by_season(df, timeframe):
        '''
        Calculate the percentage of dust events starting in december of the year before the timeframe starts and ending in november of the last year

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing a single stations data.
        timeframe : list of strings
            List of the years to analyse

        Returns
        -------
        plot_dict : Dict
            Dict of relative dust days.

        '''
        plot_dict = {}
        timeframe_str = list(map(str,timeframe))
        df_timeframe = df[df.year.isin(timeframe_str)]
        
        df_dec = df.loc[df.year == str(min(timeframe)-1)].query("month ==12")
        dec_dust = df_dec.drop(df_dec[df_dec.dust_occ ==0].index)
        if df_dec.size == 0:
            print("No data available for Dec of " + str(min(timeframe)-1))
            #ToDo Handle this properly(also cut jan and feb maybe)
        else:
            plot_dict[str(min(timeframe)-1)+"_"+"12"] = dec_dust.size/df_dec.size
        
        for year in df_timeframe.year.unique():
            for i in np.arange(1,13):
                if year == str(max(timeframe)) and i == 12:
                    continue
                else:
                    test = df_timeframe.loc[(df_timeframe.year == year) & (df_timeframe.month == i)]
                    dust = test.drop(test[test.dust_occ == 0].index)
                    plot_dict[str(year) + "_" + str(i)] = dust.size/test.size
                
        return plot_dict
    
    @staticmethod
    def order_by_season(plot_dict):
        '''
        Group the  monthly percentage of dust days into seasons

        Parameters
        ----------
        plot_dict : Dict
            Monthly percentage of dust events. Keys are year_month
            eg. load_realtive_dust_days_by_season.

        Returns
        -------
        dust_seasonality : Dict
            2-D Dict containig seasons:{Dict of years}. Keys are season and year

        '''
        dust_seasonality = {"spring": {}, "summer": {},"fall":{},"winter":{}}
        season_label = {"3":"spring","4":"spring","5":"spring", 
                        "6":"summer","7":"summer","8":"summer",
                        "9":"fall","10":"fall","11":"fall",
                        "12":"winter","1":"winter","2":"winter"}
        for key, perc in plot_dict.items():
            year, month = key.split("_")
            
            try:
                if month in ("3","6","9"):
                    dust_seasonality[season_label[month]][year] = perc
                
                elif month in ("1","2","4","7","10","5","8","11"):
                    dust_seasonality[season_label[month]][year] += perc
                    if month in ("2","5","8","11"):
                        dust_seasonality[season_label[month]][year] /= 3
                elif month == "12":
                    dust_seasonality[season_label[month]][str(int(year)+1)] = perc
            except KeyError:
                print("KeyError" + year + "_" + month)
                continue
            
        return dust_seasonality
        
    @staticmethod
    def order_df_by_season(df,season):
        '''
         Group the  monthly percentage of dust days into seasons

        Parameters
        ----------
        df : pd.DataFrame
            Datafram containing measurements for a single station
        seasons : string

        Returns
        -------
        df2 : pd.DataFrame
            
        #dust_seasonality : Dict
            #2-D Dict containig seasons:{Dict of years}. Keys are season and year

        '''
        dust_seasonality = {"spring": {}, "summer": {},"fall":{},"winter":{}}
        season_label = {"3":"spring","4":"spring","5":"spring", 
                        "6":"summer","7":"summer","8":"summer",
                        "9":"fall","10":"fall","11":"fall",
                        "12":"winter","1":"winter","2":"winter"}
        df.month
        seas = season_label.keys(season)
        df2 = df[df.month in seas]
        return df2
        
        for key, perc in plot_dict.items():
            year, month = key.split("_")
            
            try:
                if month in ("3","6","9"):
                    dust_seasonality[season_label[month]][year] = perc
                
                elif month in ("1","2","4","7","10","5","8","11"):
                    dust_seasonality[season_label[month]][year] += perc
                    if month in ("2","5","8","11"):
                        dust_seasonality[season_label[month]][year] /= 3
                elif month == "12":
                    dust_seasonality[season_label[month]][str(int(year)+1)] = perc
            except KeyError:
                print("KeyError" + year + "_" + month)
                continue
            
        return dust_seasonality
        
    @staticmethod
    def cluster_mw1(df):
        '''
         Group the first weather reported by its first digit

        Parameters
        ----------
        df : pd.DataFrame
            Datafram containing measurements for a single station

        Returns
        -------
        cluster_dict : Dictionary of int
            Dictionary containing integers for the first digit as a string as key

        '''
        cluster = df.drop(df[pd.isna(df.MW1)].index)
        cluster_dict = {"0":0,"2":0,"3":0,"5":0, "98":0, "else":0, "0_nodust":0}
        for i in cluster.MW1:
            temp = str(i)[0:2]
            if temp[0] == "0":
                if temp in("06","07","08","09"):
                    cluster_dict["0"] +=1
                else:
                    cluster_dict["0_nodust"] +=1
            elif temp[0] == "3":
                cluster_dict["3"] += 1
            elif temp == "98":
                cluster_dict[temp] += 1
            elif temp[0] == "2":
                cluster_dict["2"] += 1
            elif temp[0] == "5":
                cluster_dict["5"] += 1
            else:
                cluster_dict["else"] += 1
        return cluster_dict
    
    @staticmethod 
    def cluster_yearly_mw1(dataframe, station_id,list_of_codes= ["06","07","08"]):
        '''
         Find the number of events reported for each of a list of SYNOP Codes

        Parameters
        ----------
        df : pd.DataFrame
            Datafram containing measurements for a single station
        station_id : int
            Unique station identifier
        list_of_codes : list of strings
            List of SYNOP weather codes 

        Returns
        -------
        cluster_dict : Dictionary
            Dictionary containing integers with SYNOP weather codes as string as key

        '''        
        df = dataframe[dataframe.STATION == station_id]
        cluster = df.drop(df[pd.isna(df.MW1)].index)
        
        cluster_dict = {}
        for i in cluster.values:
            mw1 = str(i[4])[:2]
            mw2 = str(i[5])[:2]
            year = i[2]
            if mw1 in(list_of_codes):
                if year in cluster_dict.keys():
                    cluster_dict[i[2]] +=1
                else:
                    cluster_dict[i[2]] =1
            elif mw2 in (list_of_codes):
                if year in cluster_dict.keys():
                    cluster_dict[i[2]] +=1
                else:
                    cluster_dict[i[2]] =1
        
        return cluster_dict
