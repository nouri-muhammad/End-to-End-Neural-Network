import dill
import numpy as np
import os
import pandas as pd
import sys
from houseRentANN.exception import CustomException
from houseRentANN.logger import logging
from pymongo import MongoClient


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fixes all data types from different columns in raw data
    :param df: The saved pandas dataframe.
    :return: The cleaned data frame.
    """
    numeric_cols = ['size', 'maintenance_fee', 'monthly_cost', 'deposit', 'security_deposit', 'key_money', 'agency_fee',
                    'guarantor_fee', 'fire_insurance', 'other', 'year_built', 'renewal_fee']
    df.loc[df['renewal_fee'] == "1 month's rent", 'renewal_fee'] = df['rent']
    for col in numeric_cols:
        df[col] = df[col].str.replace(',', '')
        df[col] = df[col].str.replace(' negotiable', '')
        df[col] = df[col].astype(float)
    return df


def floor_number(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function receives the floor column, extracts unit floor and total floors of the building.
    Creates one new columns for each one and drops the original column.
    :param df: pandas dataframe
    :return: pandas dataframe
    """
    df['unit_floor'] = df['floor'].apply(lambda x: x[:x.find(",")] if x is not None else np.nan)
    df['total_floors'] = df['floor'].apply(lambda x:  x[x.find(",")+1:] if x is not None else np.nan)
    df = df.drop(columns='floor', axis=1)
    unit_most_freq = df['unit_floor'].value_counts().keys()[0]
    total_most_freq = df['total_floors'].value_counts().keys()[0]
    df['unit_floor'] = (df['unit_floor'].apply(lambda x: unit_most_freq if x == '' else x))
    df['unit_floor'] = (df['unit_floor'].apply(lambda x: -1 if x == 'B1' else x))
    df['total_floors'] = df['total_floors'].apply(lambda x: total_most_freq if x == '' else x)

    df['unit_floor'] = df['unit_floor'].astype(float)
    df['total_floors'] = df['total_floors'].astype(float)
    return df


def location_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function receives the location column which contains three piece of information.
    neighborhood, area, city
    saves city in a different column and removes the original column.
    :param df: pandas dataframe.
    :return: pandas dataframe.
    """
    df['location'] = df['location'].apply(lambda x: x.strip().split(","))
    # df['neighborhood'] = df['location'].apply(lambda x: x[1] if len(x) >= 2 else np.nan)  #too many unique values(243)
    df['city'] = df['location'].apply(lambda x: x[2] if len(x) >= 3 else np.nan)
    df = df.drop(columns='location', axis=1)
    return df


def closest_station_distance(df: pd.DataFrame) -> pd.DataFrame:
    df['transportation'] = df['transportation'].apply(lambda x: x[0][:x[0].find(' ')] if len(x) > 0 else np.nan)
    df['transportation'] = pd.to_numeric(df['transportation'], errors='coerce')
    df['nearest_station_distance'] = pd.to_numeric(df['nearest_station_distance'], errors='coerce')
    most_freq = df['nearest_station_distance'].value_counts().keys()[0]
    df['nearest_station_distance'] = df['nearest_station_distance'].fillna(df['transportation'])
    df['nearest_station_distance'] = df['nearest_station_distance'].fillna(most_freq)
    return df


def save_object(file_path, obj) -> None:
    """
    Saves an object as a pickle file in the specified file path.
    :param file_path: the file path to save the object.
    :param obj: the object to save.
    :return: None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file=file_path, mode="wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


class ReadRawData:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="apartments", collection_name="apartment"):
        """
        Initialize a new `ReadRawData` instance to read scraped (raw) data from MongoDB database.
        :param mongo_uri:   The MongoDB connection string in the format of mongodb://username:password@host:port.
                            Defaults to the local MongoDB instance at mongodb://localhost:27017/.
        :param db_name: The name of the database. Default to `apartments`
        :param collection_name: The name of the collection. Default to `apartment`.
        """
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]

    def read_data(self, query={}):
        """
        Read raw data from MongoDB collection.
        :param query: A query dictionary to filter the data. Default to empty
        :return: A list of documents that matches the query.
        """
        collection = self.db[self.collection_name]
        # data = list(collection.find())
        data = pd.DataFrame(collection.find(query))
        return data

    def close_connection(self):
        """
        Closes the connection to the MongoDB database.
        """
        self.client.close()
