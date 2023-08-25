import pickle
from flask import Flask, request, jsonify



with open('lin_reg.bin', 'rb') as f_in:
    (dv, scaler, model) = pickle.load(f_in)


def predict(features):

    X = dv.transform(features)
    scaled_X = scaler.transform(X)
    preds = model.predict(scaled_X)
    return float(round(preds[0], 2))

app = Flask('traffic-volume-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()
    pred = predict(features)

    result = {
                'traffic volume': pred
                }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= 9696)