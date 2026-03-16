import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib

# Load dataset
data = pd.read_csv("predictive_maintenance.csv")

print("Dataset columns:", data.columns)

# Convert Type column (L, M, H) to numeric
encoder = LabelEncoder()
data['Type'] = encoder.fit_transform(data['Type'])

# Select input features
X = data[['Type',
          'Air temperature [K]',
          'Process temperature [K]',
          'Rotational speed [rpm]',
          'Torque [Nm]',
          'Tool wear [min]']]

# Target column (IMPORTANT FIX)
y = data['Machine failure']

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# reshape for LSTM [samples, time steps, features]
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

# Build LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(1, X_scaled.shape[2])))
model.add(Dense(1, activation='sigmoid'))

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train model
model.fit(X_scaled, y, epochs=10, batch_size=32)

# Save model and preprocessors
model.save("lstm_model.h5")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(encoder, "type_encoder.pkl")

print("LSTM model saved successfully")