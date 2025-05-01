# ml_etl_package/predict.py
import numpy as np

def predict(model, scaler, input_data):
    input_scaled = scaler.transform(np.array(input_data).reshape(1, -1))
    return model.predict(input_scaled)[0]