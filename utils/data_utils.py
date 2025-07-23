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
        #ToDo: list or dict?
        #Dict so I can handle the different lengths
        #ToDo: does year always work?
        years = df.year.unique()
        no_occur = {}
        for i in years:
            temp = df.drop(df[df.year != i].index)
            no_occur[i] = temp.year.size
        return no_occur
             
    @staticmethod    
    def calc_relative_dust_days(df, station_id=False, timeframe = None):
        '''
        
    
        Parameters
        ----------
        df : pd.DataFrame
            DESCRIPTION.
        station_id : int
            DESCRIPTION.
    
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
            #ToDo Test this
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
            #plot_dict[str(year)+"_"+"12"]
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
    def load_climate_index(path="/media/tow_lin/E4A8-F53C/BA/ISD_data/",name=["NAO","ENSO"],timeframe = None):
        '''
        

        Parameters
        ----------
        name : str
            Choose a climate index between ["NAO","ENSO"].
        path : str
            DESCRIPTION.

        Returns
        -------
        climate_index : dict
            Dictionary with monthly climate index.

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
        

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing a single stations data.
        timeframe : TYPE
            DESCRIPTION.

        Returns
        -------
        plot_dict : Dict
            Dict of relative dust days .

        '''
        plot_dict = {}
        timeframe_str = list(map(str,timeframe))
        df_timeframe = df[df.year.isin(timeframe_str)]
        
        #df_dec = df[df.year == str(min(timeframe)-1)][df.month == 12]
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
        

        Parameters
        ----------
        plot_dict : Dict
            eg. load_realtive_dust_days_by_season.

        Returns
        -------
        dust_seasonality : Dict
            2-D Dict containig seasons:{Dict of years}.

        '''
        dust_seasonality = {"spring": {}, "summer": {},"fall":{},"winter":{}}
        season_label = {"3":"spring","4":"spring","5":"spring", 
                        "6":"summer","7":"summer","8":"summer",
                        "9":"fall","10":"fall","11":"fall",
                        "12":"winter","1":"winter","2":"winter"}
        for key, perc in plot_dict.items():
            year, month = key.split("_")
            
            try:
                if month in ("3","6","9"):#,"06","09","12"):
                    dust_seasonality[season_label[month]][year] = perc
                
                elif month in ("1","2","4","7","10","5","8","11"):#,"5"):
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
        

        Parameters
        ----------
        df : pd.DataFrame
            df with one Station

        Returns
        -------
        dust_seasonality : Dict
            2-D Dict containig seasons:{Dict of years}.

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
                if month in ("3","6","9"):#,"06","09","12"):
                    dust_seasonality[season_label[month]][year] = perc
                
                elif month in ("1","2","4","7","10","5","8","11"):#,"5"):
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
        #ToDo Split code for rain
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
        '''df = dataframe[dataframe.STATION == station_id]
        cluster_dict = {}
        cluster = df.drop(df[pd.isna(df.MW1)].index)
        for year in cluster.year:
            #cluster_dict[year] = 0
            temp = cluster.drop(cluster[str(cluster.MW1)[0:2] in ("06","07","08","09")].query("year" == year).index)
            print(temp.size)
            cluster_dict[year] = temp.size
            for i in cluster.MW1:
                temp = str(i)[:2]
                if temp in("06","07","08","09"):
                    cluster_dict[year] += 1'''
        #station_data = df[df.STATION == station_id]
        #all_events = data_utils.get_number_of_events(station_data)
        
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