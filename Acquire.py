'''
Functions to acquire data for clustering exercises.
Includes Zillow and Mall Data
Functions to connect to SQL, Acquire Zillow and Mall data, and count null percentages in a df.
'''

######################################## Imports ##############################################
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from env import host, username, password
###############################################################################################

############################## Connect to SQL Database ########################################
def get_db_url(db_name):

    '''
    Connect to the SQL database with credentials stored in env file.
    Function parameter is the name of the database to connect to.
    Returns url.
    '''
    
    # Creates the url and the function returns this url
    url = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    return (url)
###############################################################################################

############################## Acquire Home data ##############################################
def get_home_data():

    '''
    Connect to SQL Database with url function called within this function.
    Checks if database is already saved to computer in csv file.
    If no file found, saves to a csv file and assigns database to df variable.
    If file found, just assigns database to df variable.
    Returns df variable holding the  Home Value database.
    Includes all 52 Columns.
    '''
    
    # data_name allows the function to work no matter what a user might have saved their file name as
    # First, we check if the data is already stored in the computer
    # First conditional runs if the data is not already stored in the computer
    if os.path.isfile('zillow_home.csv') == False:

        # Querry selects the whole predicstion_2017 table from the database
        sql_querry = '''
                        SELECT *
                        FROM properties_2017
                        JOIN (SELECT id, logerror, pid, tdate FROM predictions_2017 AS pred_2017
                        JOIN (SELECT parcelid AS pid, Max(transactiondate) AS tdate FROM predictions_2017 GROUP BY parcelid) AS sq1
                        ON (pred_2017.parcelid = sq1.pid AND pred_2017.transactiondate = sq1.tdate)) AS sq2
                        ON (properties_2017.parcelid = sq2.pid)
                        LEFT JOIN airconditioningtype USING (airconditioningtypeid)
                        LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
                        LEFT JOIN buildingclasstype USING (buildingclasstypeid)
                        LEFT JOIN heatingorsystemtype USING (heatingorsystemtypeid)
                        LEFT JOIN propertylandusetype USING (propertylandusetypeid)
                        LEFT JOIN storytype USING (storytypeid)
                        LEFT JOIN typeconstructiontype USING (typeconstructiontypeid)
                        LEFT JOIN unique_properties USING (parcelid)
                        WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
                    '''

        # Connecting to the data base and using the query above to select the data
        # the pandas read_sql function reads the query into a DataFrame
        df = pd.read_sql(sql_querry, get_db_url('zillow'))

        # If any duplicates found, this removes them
        # df.columns.duplicated() returns a boolean array, True for a duplicate or False if it is unique up to that point
        # Use ~ to flip the booleans and return the df as any columns that are not duplicated
        # df.loc accesses a group of rows and columns by label(s) or a boolean array
        df = df.loc[:,~df.columns.duplicated()]
        df = df.drop('pid',axis=1)

        # The pandas to_csv function writes the data frame to a csv file
        # This allows data to be stored locally for quicker exploration and manipulation
        df.to_csv('zillow_home.csv')

    # This conditional runs if the data has already been saved as a csv (if the function has already been run on your computer)
    else:
        # Reads the csv saved from above, and assigns to the df variable
        df = pd.read_csv('zillow_home.csv', index_col=0)

    return df
###############################################################################################

############################## Acquire Mall data ##############################################
def get_mall_data():

    '''
    Connect to SQL Database with url function called within this function.
    Checks if database is already saved to computer in csv file.
    If no file found, saves to a csv file and assigns database to df variable.
    If file found, just assigns database to df variable.
    Returns df variable holding the  Mall data.
    '''
    
    # data_name allows the function to work no matter what a user might have saved their file name as
    # First, we check if the data is already stored in the computer
    # First conditional runs if the data is not already stored in the computer
    if os.path.isfile('mall_customers.csv') == False:

        # Querry selects the whole predicstion_2017 table from the database
        sql_querry = '''
                        SELECT *
                        FROM customers;
                    '''

        # Connecting to the data base and using the query above to select the data
        # the pandas read_sql function reads the query into a DataFrame
        df = pd.read_sql(sql_querry, get_db_url('mall_customers'))

        # If any duplicates found, this removes them
        # df.columns.duplicated() returns a boolean array, True for a duplicate or False if it is unique up to that point
        # Use ~ to flip the booleans and return the df as any columns that are not duplicated
        # df.loc accesses a group of rows and columns by label(s) or a boolean array
        df = df.loc[:,~df.columns.duplicated()]

        # The pandas to_csv function writes the data frame to a csv file
        # This allows data to be stored locally for quicker exploration and manipulation
        df.to_csv('mall_customers.csv')

    # This conditional runs if the data has already been saved as a csv (if the function has already been run on your computer)
    else:
        # Reads the csv saved from above, and assigns to the df variable
        df = pd.read_csv('mall_customers.csv', index_col=0)

    return df
###############################################################################################

################################### DF Nulls ##################################################
def null_counts(df):
    '''
    Return a df of null counts in each columns and the percentage of nulls
    '''
    rows = df.shape[0]
    nulls = pd.DataFrame(df.isnull().sum())
    nulls.columns = ['null_count']
    nulls['null_percentage'] = (nulls / rows) * 100
    return nulls
###############################################################################################