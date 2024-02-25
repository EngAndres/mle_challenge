"""This file should contain the ML model class."""

from datetime import datetime
from typing import List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import xgboost as xgb


class DelayModel:

    def __init__(self):
        self._model = None  # Model should be saved in this attribute.
        self.train_model()

    def get_period_day(self, date) -> str:
        """
        Get period of the day from a date.

        Args:
            date (str): date in format "YYYY-MM-DD HH:MM:SS".

        Returns:
            str: period of the day.
        """
        date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").time()
        morning_min = datetime.strptime("05:00", "%H:%M").time()
        morning_max = datetime.strptime("11:59", "%H:%M").time()
        afternoon_min = datetime.strptime("12:00", "%H:%M").time()
        afternoon_max = datetime.strptime("18:59", "%H:%M").time()
        evening_min = datetime.strptime("19:00", "%H:%M").time()
        evening_max = datetime.strptime("23:59", "%H:%M").time()
        night_min = datetime.strptime("00:00", "%H:%M").time()
        night_max = datetime.strptime("4:59", "%H:%M").time()

        if date_time > morning_min and date_time < morning_max:
            return "mañana"
        elif date_time > afternoon_min and date_time < afternoon_max:
            return "tarde"
        elif (date_time > evening_min and date_time < evening_max) or (
            date_time > night_min and date_time < night_max
        ):
            return "noche"

    def is_high_season(self, fecha) -> bool:
        """This function returns 1 if the date is in high season, 0 otherwise.

        Args:
            fecha (str): date in format "YYYY-MM-DD HH:MM:SS".

        Returns:
            bool: 1 if the date is in high season, 0 otherwise.
        """
        fecha_anio = int(fecha.split("-")[0])
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        range1_min = datetime.strptime("15-Dec", "%d-%b").replace(year=fecha_anio)
        range1_max = datetime.strptime("31-Dec", "%d-%b").replace(year=fecha_anio)
        range2_min = datetime.strptime("1-Jan", "%d-%b").replace(year=fecha_anio)
        range2_max = datetime.strptime("3-Mar", "%d-%b").replace(year=fecha_anio)
        range3_min = datetime.strptime("15-Jul", "%d-%b").replace(year=fecha_anio)
        range3_max = datetime.strptime("31-Jul", "%d-%b").replace(year=fecha_anio)
        range4_min = datetime.strptime("11-Sep", "%d-%b").replace(year=fecha_anio)
        range4_max = datetime.strptime("30-Sep", "%d-%b").replace(year=fecha_anio)

        if (
            (fecha >= range1_min and fecha <= range1_max)
            or (fecha >= range2_min and fecha <= range2_max)
            or (fecha >= range3_min and fecha <= range3_max)
            or (fecha >= range4_min and fecha <= range4_max)
        ):
            return 1
        else:
            return 0

    def get_min_diff(self, data):
        """
        This function returns the difference in minutes between two dates.

        Args:
            data (dict): dictionary with two keys: 'Fecha-O' and 'Fecha-I'.

        Returns:
            float: difference in minutes between two dates.
        """
        fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
        fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
        return min_diff

    def train_model(self) -> None:
        """Train the model based on the data and right functions call."""
        # Load data
        data = pd.read_csv("data/data.csv")

        # Preprocess data
        features, target = self.preprocess(data, "delay")

        # Generate training data, test data and target
        x_train, x_test, y_train, y_test = train_test_split(
            features, target, test_size=0.33, random_state=42
        )

        # Fit model
        self.fit(x_train, y_train)

    def preprocess(
        self, data: pd.DataFrame, target_column: str = None
    ):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """

        data["period_day"] = data["Fecha-I"].apply(self.get_period_day)
        data["high_season"] = data["Fecha-I"].apply(self.is_high_season)
        data["min_diff"] = data.apply(self.get_min_diff, axis=1)

        threshold_in_minutes = 15
        data["delay"] = np.where(data["min_diff"] > threshold_in_minutes, 1, 0)

        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        target = data[target_column]

        return features, target

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        # define balance
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0 / n_y1

        # create a XGBoost balanced model
        self._model = xgb.XGBClassifier(
            random_state=1, learning_rate=0.01, scale_pos_weight=scale
        )
        self._model.fit(features, target)

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        return list(self._model.predict(features))
