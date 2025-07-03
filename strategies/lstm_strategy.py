import numpy as np
import pandas as pd
import torch
print("Torch OK")
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        x = self.fc1(lstm_out[:, -1, :])
        x = self.relu(x)
        return self.fc2(x)


def prepare_data(df, window_size=30):
    close = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    close_scaled = scaler.fit_transform(close)

    X, y = [], []
    for i in range(window_size, len(close_scaled)):
        X.append(close_scaled[i - window_size:i])
        y.append(close_scaled[i])

    X = np.array(X)
    y = np.array(y)

    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32), scaler


def train_and_predict(df, window_size=30, epochs=100):
    X, y, scaler = prepare_data(df, window_size)

    model = LSTMModel()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        pred = model(X).numpy()

    pred_unscaled = scaler.inverse_transform(pred)
    actual_unscaled = scaler.inverse_transform(y.numpy())

    df_result = df.copy()
    df_result = df_result.iloc[window_size:]
    df_result['Predicted Close'] = scaler.inverse_transform(pred)
    df_result['Actual Close'] = actual_unscaled

    return df_result
