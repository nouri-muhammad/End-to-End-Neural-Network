import os
import sys
from houseRentANN.exception import CustomException
from houseRentANN.logger import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


class ModelTrainer:
    def __init__(self, x_train_arr, y_train_arr, x_test_arr, y_test_arr):
        self.x_train_arr = x_train_arr
        self.y_train_arr = y_train_arr
        self.x_test_arr = x_test_arr
        self.y_test_arr = y_test_arr

    def initiate_model_trainer(self) -> None:
        try:
            logging.info("Creating the Model")
            model = Sequential()

            model.add(Dense(units=101, activation='relu'))
            model.add(Dropout(rate=0.4))
            model.add(Dense(units=101, activation='relu'))
            model.add(Dropout(rate=0.4))
            model.add(Dense(units=202, activation='relu'))
            model.add(Dropout(rate=0.3))
            model.add(Dense(units=202, activation='relu'))
            model.add(Dropout(rate=0.3))
            model.add(Dense(units=101, activation='relu'))
            model.add(Dropout(rate=0.4))
            model.add(Dense(units=101, activation='relu'))
            model.add(Dropout(rate=0.4))
            model.add(Dense(units=101, activation='relu'))
            model.add(Dropout(rate=0.4))
            model.add(Dense(units=1, activation='relu'))

            model.compile(loss='mse', optimizer='adam')

            logging.info("Train the Model")
            early_stop = EarlyStopping(
                monitor='val_loss',
                mode='min',
                verbose=1,
                patience=20
            )
            model.fit(
                x=self.x_train_arr,
                y=self.y_train_arr,
                validation_data=(self.x_test_arr, self.y_test_arr),
                batch_size=256,
                epochs=6000,
                callbacks=[early_stop]
            )

            # explained variance score = 0.945 ~ 0.95   =>   for this model
            # mean absolute error = 12095

            logging.info("Save the Model")
            model_file_path = os.path.join("data", "model.keras")
            model.save(model_file_path)

        except Exception as e:
            raise CustomException(e, sys)
