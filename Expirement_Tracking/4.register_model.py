import argparse
import os
import pickle

import mlflow
from hyperopt import hp, space_eval
from hyperopt.pyll import scope
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


mlflow_experiment_name_hyperopt = "trafic-volume-prediction-hyperopt"

os.environ["AZURE_STORAGE_ACCESS_KEY"] = "your Azure keysecrets"
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = "your Azure connection string"

# set to your server URI
remote_server_uri = "0.0.0.0" 
mlflow_tracking_uri = "sqlite:///mlflow.db"
mlflow.set_tracking_uri(f"http://{remote_server_uri}:5000")

mlflow_experiment_name = "traffic-volume-rf-best-models"
mlflow.set_experiment(mlflow_experiment_name)
mlflow.sklearn.autolog()

space = {
            'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
            'n_estimators': scope.int(hp.quniform('n_estimators', 10, 50, 1)),
            'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 10, 1)),
            'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 4, 1)),
            'random_state': 42
        }


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def train_and_log_model(data_path, params):
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    X_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))

    with mlflow.start_run():
        params = space_eval(space, params)
        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)

        # evaluate model on the validation and test sets
        valid_rmse = mean_squared_error(y_val, rf.predict(X_val), squared=False)
        mlflow.log_metric("valid_rmse", valid_rmse)
        test_rmse = mean_squared_error(y_test, rf.predict(X_test), squared=False)
        mlflow.log_metric("test_rmse", test_rmse)


def main(data_path):

    client = MlflowClient()

    # retrieve the top model runs
    experiment = client.get_experiment_by_name(mlflow_experiment_name_hyperopt)
    runs = client.search_runs(
                                experiment_ids=experiment.experiment_id,
                                run_view_type=ViewType.ACTIVE_ONLY,
                                max_results=5,
                                order_by=["metrics.rmse ASC"]
                                )
    

    for run in runs:
        train_and_log_model(data_path=data_path, params=run.data.params)

    # select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name(mlflow_experiment_name)

    best_run = MlflowClient().search_runs(
                                            experiment_ids=experiment.experiment_id,
                                            run_view_type=ViewType.ACTIVE_ONLY,
                                            max_results=1,
                                            order_by=["metrics.test_rmse ASC"]
                                            )[0]
    
    run_id = best_run.info.run_id
    model_uri = f"runs:/{run_id}/model"
    
    mlflow.register_model(
                            model_uri = model_uri,
                            name = "sklearn-random-forest-regressor"
                            )




if __name__ == '__main__':


    data_path = "./datasets"

    main(data_path)