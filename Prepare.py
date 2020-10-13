############################################### Imports ###########################################
import Acquire

import pandas as import pd
import numpy as np
###################################################################################################

####################################### Remove Nulls in DF ########################################
def remove_nulls(df, col_percent, row_percent):

    '''
    col_percent and row_percent are parameters to determine the cutoff for removing columns and rows.
    If column or row has higher percentage of nulls than specified, they are removed.
    Works on any df passed in parameter.
    '''

    # removing columns, loops through columns in df
    for col in df.columns:
        
        # calculates percentage of nulls by column
        nulls = df[col].isnull().sum()
        rows = df.shape[0]
        percent = (nulls / rows)
        
        # if percentage greater than specified col_percent
        if percent >= col_percent:
            
            # drops the column
            df = df.drop(col, axis=1)
         
    # removing observations, loops through rows in df   
    for row in df.index:
        
        # calculates percentage of nulls by row
        nulls = df[df.index == [row]].isnull().sum().sum()
        cols = df.shape[1]
        percent = (nulls / cols)
        
        # if percentage greater than specified row_percent
        if percent > row_percent:
            
            #drops the row
            df = df.drop(df.index[row])
            
    return df
###################################################################################################

####################################### Prepare Zillow Data #######################################
def prepare_zillow(col_percent, row_percent):

    '''
    Prepares zillow dataframe.
    Removes properties that are not single-unit.
    Removes null columns and rows based on percent of nulls specified in parameters.
    Drops any remaining nulls.
    '''

    # acquire df from .py module
    df = Acquire.get_home_data()

    # include only single-unit properties by id number
    df = df[(df['propertylandusetypeid'] == 262) |
            (df['propertylandusetypeid'] == 266) |
            (df['propertylandusetypeid'] == 74) |
            (df['propertylandusetypeid'] == 58) |
            (df['propertylandusetypeid'] == 37) |
            (df['propertylandusetypeid'] == 6)]

    # calling function to remove nulls in columns and rows
    df = remove_nulls(df, col_percent, row_percent)

    # fills any leftover nulls by columns most frequent value
    for col in df.columns:
    df = df.fillna(df[col].value_counts().index[0])

    return df
###################################################################################################

######################################## Prepare Mall Data ########################################



###################################################################################################