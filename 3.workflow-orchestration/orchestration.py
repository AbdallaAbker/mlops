import pandas as pd
import numpy as np
import os
import pickle
import mlflow
from prefect import flow, task

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# set to your server URI
remote_server_uri_locally = "0.0.0.0" 
remote_server_uri_Azure_Cloud = "mlflowzoomcamp.westus2.cloudapp.azure.com"  #AZURE_CLOUD_DEPLOYMENT
mlflow_tracking_uri = "sqlite:///mlflow.db"
mlflow.set_tracking_uri(f"http://{remote_server_uri_locally}:5000")
mlflow_experiment_name = "trafic-volume-prediction-train"
mlflow.set_experiment(mlflow_experiment_name)

@task
def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)
@flow
def load_data(data_path):
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    return X_train, y_train, X_val, y_val



@flow
def main_flow(data_path):

    mlflow_tracking_uri = "sqlite:///mlflow.db"
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow_experiment_name = "trafic-volume-prediction-train"
    mlflow.set_experiment(mlflow_experiment_name)

    X_train, y_train, X_val, y_val = load_data(data_path)

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_val)

    mean_squared_error(y_val, y_pred, squared=False)


    rmse = mean_squared_error(y_val, y_pred, squared = False)

    return rmse


if __name__ == "__main__":

    data_path = "./datasets"

    main_flow(data_path)
