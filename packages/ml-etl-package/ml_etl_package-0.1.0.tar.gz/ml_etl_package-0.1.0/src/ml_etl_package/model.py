# ml_etl_package/model.py
from sklearn.linear_model import LinearRegression
import joblib

def train_and_save_model(X, y, model_path="model.pkl"):
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"✅ Model saved to {model_path}")

def load_model(model_path="model.pkl"):
    return joblib.load(model_path)