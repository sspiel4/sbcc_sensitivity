# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 17:03:36 2020

@author: scott

Hospital was dropped because there was no sensitivity run.

"""

import os
import pandas as pd

# get each building type
cwd = os.getcwd()
bldgTypes = os.listdir(cwd)
bldgTypes.remove('increments.csv')
bldgTypes.remove('00_archived_code')
bldgTypes.remove('main_wrking.py')
bldgTypes.remove('categories.csv')
bldgTypes.remove('01_results')

# import increments
incr = pd.read_csv(os.getcwd() + '\\increments.csv')

# create empty dictionaries and lists for data
results = {}
bldgTypeList = []
attrList = []
attrCat = []
valList = []

cats = {'air_leakage':0.1, 'setpoint':1, 'equipment_density':0.1, 'dhw':0.1, 
        'gas':100000, 'lighting_density':0.1, 'oa_person':5, 'oa_area':0.05}

# loop through building types
for bldgType in bldgTypes:
    
    path = cwd + '\\' + bldgType + '\\sensitivity\\'
    params = pd.read_csv(path + 'parameters.csv')
    sens = pd.read_csv(path + 'sensitivity.csv')
        
    # create list of attributes use in sensitivity on building type
    attrs = params['key'].tolist()
    
    for attr in attrs:
        # check if attribute has category
        for key in cats:
            if key in attr:
                #print(attr + ' has category with increment ' + str(cats[key]))

                # find index of item in list
                index = params['key'].tolist().index(attr)
                # find range of values
                rnge = float(params.iloc[index, 4]) - float(params.iloc[index, 3])
            
                if attr in sens['Parameter'].tolist():
                    index = sens['Parameter'].tolist().index(attr)
                    percentChange = sens.iloc[index, 1]
                    
                    #print(bldgType + attr)
                    incr_val_bigladder = float(percentChange) / 5  #* cats[key] / float(rnge)
                    #incr_val_ecotope = float(percentChange) * cats[key] / float(rnge)
            
                    # append itesms to lists
                    bldgTypeList.append(bldgType)
                    attrList.append(attr)
                    attrCat.append(key)
                    valList.append(incr_val_bigladder)
                    
                else:
                    print(attr + " is missing from " + bldgType + " sensitivity.csv")
            

df = pd.DataFrame()
df['Building Type'] = bldgTypeList
df['Attribute'] = attrList
df['Attribute Type'] = attrCat
df['Incremental Change'] = valList

results = df.groupby(['Building Type','Attribute Type'])['Incremental Change'].apply(lambda x : x.astype(float).sum())

results.to_csv(os.getcwd() + '\\01_results\\20200621_BigLadderResults.csv')





