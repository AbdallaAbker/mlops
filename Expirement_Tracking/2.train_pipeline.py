import pandas as pd
import numpy as np
import os
import pickle
import mlflow

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

os.environ["AZURE_STORAGE_ACCESS_KEY"] = "your Azure keysecrets"
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "your Azure connection string"

# set to your server URI
remote_server_uri = "0.0.0.0" 
mlflow_tracking_uri = "sqlite:///mlflow.db"
mlflow.set_tracking_uri(f"http://{remote_server_uri}:5000")


# set MLflow experiment
mlflow_experiment_name = "trafic-volume-prediction-train"
mlflow.set_experiment(mlflow_experiment_name)


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
