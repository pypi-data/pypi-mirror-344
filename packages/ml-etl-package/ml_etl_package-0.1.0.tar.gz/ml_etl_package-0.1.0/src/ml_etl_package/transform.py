# ml_etl_package/transform.py
from sklearn.preprocessing import StandardScaler

def transform(df, feature_cols=["sqft", "bedrooms", "bathrooms"], target_col="price"):
    df = df.dropna()
    X = df[feature_cols]
    y = df[target_col]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler