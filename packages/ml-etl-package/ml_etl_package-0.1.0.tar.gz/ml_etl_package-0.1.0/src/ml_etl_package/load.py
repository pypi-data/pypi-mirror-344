# ml_etl_package/load.py
import pandas as pd

def save_to_csv(X, y, filename="transformed_data.csv"):
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
    df["target"] = y.reset_index(drop=True)
    df.to_csv(filename, index=False)
    print(f"✅ Transformed data saved to {filename}")