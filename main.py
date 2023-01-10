from flask import Flask, jsonify, request
from flask.logging import create_logger
import logging
import pandas as pd
import pickle
import warnings
warnings.simplefilter("ignore", UserWarning)

app = Flask(__name__)

LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# Load model, scaler, and column transformer
model = pickle.load(open('model/model_lr.pkl','rb'))
scaler = pickle.load(open('model/scaler.pkl','rb'))
transformer = pickle.load(open('model/column_transformer.pkl','rb'))

def make_prediction(model, data, scaler, transformer):
    x_new = data.values

    # Set numerical columns
    numerical_cols = [0, 3, 4, 7, 9, 11]

    x_new[:, numerical_cols] = scaler.transform(x_new[:, numerical_cols])
    x_new = transformer.transform(x_new)

    # Make prediction
    new_preds = model.predict(x_new)

    new_preds = ['Not at Risk' if pred == 0 else 'At Risk' for pred in new_preds]

    return new_preds

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Welcome to our Web App on Predicting Risk of a heart attack'


@app.route('/predict', methods = ['POST'])
def predict():
    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    data = pd.DataFrame(json_payload)
    LOG.info(f"inference payload DataFrame: {data}")
    prediction = make_prediction(model, data, scaler, transformer)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
