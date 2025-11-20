import os
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/dataset.csv"
MODEL_PATH = "models/weather_lstm_final.keras"
SCALER_PATH = "models/weather_scaler.pkl"
INPUT_WINDOW = 14
OUTPUT_HORIZON = 7

# -------------------------
# LOAD MODEL + SCALER
# -------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Missing model → {MODEL_PATH}")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Missing scaler → {SCALER_PATH}")

print("Loading model + scaler...")
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(DATA_PATH)
df["Date_parsed"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

features = ["AT", "WS", "RH", "BP", "SR"]
data = df[features].dropna()

# Scale data
scaled = scaler.transform(data)

# -------------------------
# LAST 14 DAYS INPUT
# -------------------------
X_input = scaled[-INPUT_WINDOW:]
X_input = np.array(X_input).reshape(1, INPUT_WINDOW, len(features))

# -------------------------
# PREDICT
# -------------------------
output = model.predict(X_input)
output = output.reshape(OUTPUT_HORIZON, len(features))

# Inverse scale each timestep
output_unscaled = scaler.inverse_transform(output)

print("\n====== 7-DAY WEATHER FORECAST (UNSCALED) ======\n")
forecast_df = pd.DataFrame(output_unscaled, columns=features)
print(forecast_df)
