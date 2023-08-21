import pandas as pd
import numpy as np
import os
import pickle
import mlflow

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# AZURE_STORAGE_ACCESS_KEY="+gxk+KoIUMgkNPa8ZW80QOaswHagYTr2r7ZZXuYBdKqEnTkrO27J4tVtchE2hsp83qL7EIDDUsAz+AStrXElww=="
# Set the Azure Blob Storage connection string
# os.environ["AZURE_STORAGE_CONNECTION_STRING"] = ""

# tracking_uri = '20.9.177.115:8080'
# Set the MLflow tracking URI to use Azure Blob Storage
mlflow.set_tracking_uri("http://20.9.177.115:5000")

# mlflow.set_tracking_uri("sqlite:///mlflow.db")  #http://127.0.01:5000
mlflow.set_experiment("trafic-volume-prediction-train")

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

def run_expirement(data_path):

    mlflow.sklearn.autolog()

    with mlflow.start_run():

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        lr = LinearRegression()
        lr.fit(X_train, y_train)

        y_pred = lr.predict(X_val)

        mean_squared_error(y_val, y_pred, squared=False)


        rmse = mean_squared_error(y_val, y_pred, squared = False)

        mlflow.log_metric("rmse", rmse)


if __name__ == "__main__":

    data_path = "./datasets"

    run_expirement(data_path)
