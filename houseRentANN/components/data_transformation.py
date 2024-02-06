import sys
from houseRentANN.exception import CustomException
from houseRentANN.logger import logging
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


class DataTransformation:
    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train.values
        self.y_test = y_test.values

    def get_transformation_obj(self) -> object:
        try:
            numerical_cols = list(self.x_train.select_dtypes(include=['float']).columns)
            categorical_cols = list(self.x_train.select_dtypes(include=['object']).columns)

            logging.info("Scaling Numerical Columns")
            num_pipeline = Pipeline(
                steps=[
                    ("scaler", MinMaxScaler())
                ]
            )
            logging.info("Scaling Categorical Columns")
            cat_pipeline = Pipeline(
                steps=[
                    ("OneHotEncoder", OneHotEncoder(handle_unknown='ignore'))
                ]
            )
            logging.info("Creating ColumnTransformer Object")
            processor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )

            return processor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Getting ColumnTransformer Object")
            preprocessor_obj = self.get_transformation_obj()

            logging.info("Apply Preprocessing Object on Train and Test Data")
            input_feature_train_arr = preprocessor_obj.fit_transform(self.x_train)
            input_feature_test_arr = preprocessor_obj.transform(self.x_test)

            logging.info("Converting x_train and x_test into Numpy Arrays")
            x_train_arr = input_feature_train_arr.toarray()
            x_test_arr = input_feature_test_arr.toarray()

            return (
                x_train_arr,
                self.y_train,
                x_test_arr,
                self.y_test
            )

        except Exception as e:
            raise CustomException(e, sys)
