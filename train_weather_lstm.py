import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/dataset.csv"
MODEL_PATH = "models/weather_lstm_final.keras"
SCALER_PATH = "models/weather_scaler.pkl"
INPUT_WINDOW = 14
OUTPUT_HORIZON = 7

os.makedirs("models", exist_ok=True)

print(f"Loading dataset: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

df["Date_parsed"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
print(df["Date_parsed"].min(), "->", df["Date_parsed"].max())

features = ["AT", "WS", "RH", "BP", "SR"]
data = df[features].dropna()

# ---- SCALE DATA ----
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)

joblib.dump(scaler, SCALER_PATH)
print(f"Scaler saved → {SCALER_PATH}")

# ---- CREATE SEQUENCES ----
X, y = [], []
N = len(scaled)
limit = N - INPUT_WINDOW - OUTPUT_HORIZON

for i in range(limit):
    X.append(scaled[i:i + INPUT_WINDOW])
    y.append(scaled[i + INPUT_WINDOW:i + INPUT_WINDOW + OUTPUT_HORIZON])

X = np.array(X)
y = np.array(y).reshape(len(y), -1)

print("X shape:", X.shape)
print("y shape:", y.shape)

# ---- LSTM MODEL ----
model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(INPUT_WINDOW, len(features))),
    LSTM(64),
    Dense(OUTPUT_HORIZON * len(features))
])

model.compile(optimizer="adam", loss="mse")

print("Training model...")
model.fit(X, y, epochs=20, batch_size=8, validation_split=0.2, verbose=1)

# ---- SAVE MODEL ----
model.save(MODEL_PATH)
print(f"Model saved → {MODEL_PATH}")
