import os
import pickle
import mlflow
import numpy as np
import xgboost as xgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

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


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def main(data_path, max_evals, num_boost_round):
    
    #disable autolog
    mlflow.sklearn.autolog(disable=True)

    #retrieve tran, validation data
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    
    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_val, label=y_val)

    def objective(params):
        with mlflow.start_run():
            mlflow.set_tag("model", "xgboost")
            mlflow.log_params(params)
            booster = xgb.train(
                                params=params,
                                dtrain=train,
                                num_boost_round=num_boost_round,
                                evals=[(valid, 'validation')],
                                early_stopping_rounds=50
                                )
            
            y_pred = booster.predict(valid)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)

        return {'loss': rmse, 'status': STATUS_OK}

    search_space = {
                    'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
                    'learning_rate': hp.loguniform('learning_rate', -3, 0),
                    'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
                    'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
                    'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
                    'objective': 'reg:linear',
                    'seed': 42
                    }
    
    #to ensure reproducibility
    rstate = np.random.default_rng(42)

    best_result = fmin(
                        fn=objective,
                        space=search_space,
                        algo=tpe.suggest,
                        max_evals = max_evals,
                        trials=Trials(),
                        rstate=rstate
                        )


if __name__ == '__main__':

    data_path = "./Expirement_Tracking/artifacts"
    max_evals = 50
    num_boost_round = 100
    
    #start
    main(data_path, max_evals, num_boost_round)