import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split

import pickle
import os

def read_df(file_location):
    df = pd.read_csv(os.path.join(file_location, "traffic.csv"))
    print(df.head())
    return df

def dump_pickle(obj, filename):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)


def generate_train_val_test_data(df):

    X = df.drop(['traffic_volume', 'holiday'], axis = 1)
    y = df['traffic_volume']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.2, random_state = 0)

    dv = DictVectorizer()

    X_train_dicts = X_train.to_dict(orient= 'records')
    X_val_dicts = X_val.to_dict(orient= 'records')
    X_test_dicts = X_test.to_dict(orient= 'records')

    X_train = dv.fit_transform(X_train_dicts)
    X_val = dv.transform(X_val_dicts)
    X_test = dv.transform(X_test_dicts)

    scaler = MaxAbsScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    # save datasets
    cwd = os.getcwd()
    output_folder = os.path.join(cwd, "Expirement_Tracking/artifacts")
    os.makedirs(output_folder, exist_ok=True)



    dump_pickle((X_train, y_train), os.path.join(output_folder, "train.pkl"))
    dump_pickle((X_val, y_val), os.path.join(output_folder, "val.pkl"))
    dump_pickle((X_test, y_test), os.path.join(output_folder, "test.pkl"))

    return None


if __name__ == "__main__":

    raw_data = "./datasets"
    #read datset and output df
    df = read_df(raw_data)
    #generate the train/val/test data
    generate_train_val_test_data(df)





