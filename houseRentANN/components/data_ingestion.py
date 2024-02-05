import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
from houseRentANN.exception import CustomException
from houseRentANN.logger import logging
from houseRentANN.utils import (
    ReadRawData,
    fix_data_types,
    floor_number,
    location_cleaning,
    closest_station_distance,
)
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self):
        self.df_obj = ReadRawData()

    def initiate_data_ingestion(self):
        try:
            logging.info("Read Raw Data From DataBase")
            df = self.df_obj.read_data()
            self.df_obj.close_connection()

            logging.info("Fixing Data Types")
            df = fix_data_types(df)

            logging.info("Drop monthly_cost, rent and total_move_in_fee Columns")
            # These columns have perfect or near perfect correlation with monthly_cost column which is predictable.
            # total_move_in_fee column is the sum of other costs including monthly_cost thus we don't need it.
            df = df.drop(columns=['total_move_in_fee', 'rent', 'price', 'other_costs'], axis=1)

            logging.info("Cleaning Columns Including Filling Null Values With Appropriate Values")
            df['security_deposit'] = df['security_deposit'].fillna(0)
            df['fire_insurance'] = df['fire_insurance'].fillna(0)
            df['other'] = df['other'].fillna(0)
            df['renewal_fee'] = df['renewal_fee'].fillna(0)
            df['short_term_stay'] = df['short_term_stay'].fillna("Not Available")
            df['short_term_stay'] = df['short_term_stay'].map({"Available": 1, "Not Available": 0})
            most_repeated = df['direction_facing'].value_counts().keys()[0]
            df['direction_facing'] = df['direction_facing'].fillna(most_repeated)
            df['nearest_station_distance'] = df['nearest_station'].apply(lambda x: x[x.find("(")+1: x.find("min")-1] if x is not None else None)
            most_repeated = df['nearest_station_distance'].value_counts().keys()[0]
            df['nearest_station_distance'] = df['nearest_station_distance'].fillna(most_repeated)

            logging.info("Object Type Data Cleaning")
            df = floor_number(df)
            df = location_cleaning(df)
            df = closest_station_distance(df)

            logging.info("Drop Unuseful Columns")
            df.drop(columns=["_id", "name", "unit_number", "nearest_station", "building_name",
                             "building_description", "other_expenses", "property_description",
                             "features", "available", "date_updated", "next_update_schedule", "stations",
                             "transportation"], axis=1, inplace=True)

            logging.info("Drop Rows with Null Values if Any Exists")
            df = df.dropna()

            logging.info("Train Test Split")
            X = df.drop(columns='monthly_cost', axis=1)
            y = df['monthly_cost']
            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=91)

            return x_train, x_test, y_train, y_test

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == '__main__':
    obj = DataIngestion()
    x_train, x_test, y_train, y_test = obj.initiate_data_ingestion()
