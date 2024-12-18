from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import psutil
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Flask App
app = Flask(__name__)

# Paths to datasets
data_paths = {
    "dataset1": "C:/path_to_data/Karachi_Climate_Data.csv",
    "dataset2": "C:/path_to_data/Karachi_2022_06_01_to_2024_12_25.csv",
    "dataset3": "C:/path_to_data/weather_data_karachi.csv",
    "dataset4": "C:/path_to_data/weather_data_karachi2.csv",
}

# Load datasets
def load_datasets():
    datasets = {}
    for name, path in data_paths.items():
        datasets[name] = pd.read_csv(path)
    return datasets

# Preprocess data for temperature prediction
def preprocess_datasets(datasets):
    processed_data = []
    for name, df in datasets.items():
        if name == "dataset1":
            temp_data = df[["tempmax", "tempmin", "temp"]]
        elif name == "dataset2":
            temp_data = df[["Tmax", "Tmin", "Tavg"]]
        elif name == "dataset3":
            temp_data = df[["TMAX", "TMIN", "TAVG"]]
        elif name == "dataset4":
            temp_data = df[["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]]
        processed_data.append(temp_data)
    
    return pd.concat(processed_data, ignore_index=True)

# Train model using RandomForestRegressor
def train_model(data):
    X = data.drop(columns=["temp"], errors='ignore')  # Features
    y = data["temp"] if "temp" in data.columns else data["TAVG"]  # Target variable
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Model MSE: {mse}, R-squared: {r2}")
    return model

# Memory usage graph
def plot_memory_usage():
    memory_info = psutil.virtual_memory()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=["Used", "Available"], y=[memory_info.used, memory_info.available])
    plt.ylabel("Memory (Bytes)")
    plt.title("Memory Usage")
    plt.savefig("static/memory_usage.png")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Load and preprocess data
    datasets = load_datasets()
    unified_data = preprocess_datasets(datasets)
    
    # Train model
    model = train_model(unified_data)
    
    # Get predictions for the next 5 days (using mean temperature as a placeholder)
    future_dates = pd.date_range(start=pd.Timestamp.today(), periods=5).to_frame(index=False, name="date")
    future_dates["tempmax"] = unified_data["tempmax"].mean()
    future_dates["tempmin"] = unified_data["tempmin"].mean()

    predictions = model.predict(future_dates.drop(columns=["date"], errors='ignore'))

    # Return results
    plot_memory_usage()
    return jsonify({
        "predictions": predictions.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
