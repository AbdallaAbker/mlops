import sys
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import pickle
import requests



dct_map = {
    'Clear': 1,
    'Clouds': 2,
    'Drizzle': 3,
    'Mist': 4,
    'Rain': 5,
    'Haze': 6,
    'Fog': 7,
    'Thunderstorm': 8,
    'Snow': 9,
    'Squall': 10,
    'Smoke': 11
}

# with open('lin_reg.bin', 'rb') as f_in:
#     model = pickle.load(f_in)

from joblib import load

# Load the model using joblib
with open('lin_reg.joblib', 'rb') as f_in:
    model = load(f_in)


def predict_volume(features):

    preds = model.predict(features)
    return float(round(preds[0], 2))

application = Flask(__name__)


app = application

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')  # Change to the correct template name
    else:
        ride_dct = {
            'temp': float(request.form.get('temp')),
            'rain_1h': float(request.form.get('rain_1h')),
            'snow_1h': float(request.form.get('snow_1h')),
            'clouds_all': int(request.form.get('clouds_all')),
            'weather_main': int(dct_map[request.form.get('weather_main')]),
            'Rush Hour': int(request.form.get('Rush Hour'))  # Corrected mapping
        }

        print(ride_dct)

        pred_df = pd.DataFrame.from_records([ride_dct])
        print(pred_df)

        results = predict_volume(pred_df)

        return render_template('home.html', results = results)  # Change to the correct template name

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9696)
