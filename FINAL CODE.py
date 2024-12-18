import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import datetime

# Load datasets
def load_data(file_path):
    return pd.read_csv(file_path)

# Paths to your datasets
paths = [
    r"C:\Users\mahad\Desktop\CLIMACAST\Karachi 2022-06-01 to 2024-12-25.csv",
    r"C:\Users\mahad\Desktop\CLIMACAST\Karachi_Climate_Data.csv",
    r"C:\Users\mahad\Desktop\CLIMACAST\weather_data_karachi.csv",
    r"C:\Users\mahad\Desktop\CLIMACAST\weather_data_karachi2.csv"
]

# Load all datasets into a single DataFrame
dataframes = [load_data(path) for path in paths]

# Handle missing Tavg column and concatenate data
for df in dataframes:
    if 'Tavg' not in df.columns:
        df['Tavg'] = (df['Tmax'] + df['Tmin']) / 2

data = pd.concat(dataframes, ignore_index=True)

# Parse dates with mixed formats
def parse_dates(date_series):
    return pd.to_datetime(date_series, errors='coerce').fillna(
        pd.to_datetime(date_series, format='%Y-%m', errors='coerce')
    )

data['date'] = parse_dates(data['date'])

# Drop rows with invalid dates
data = data.dropna(subset=['date'])

# Sort data by date
data = data.sort_values(by='date')

# Fill missing values (if any)
data.ffill(inplace=True)
data.bfill(inplace=True)

# Feature Engineering
data['day_of_year'] = data['date'].dt.dayofyear

# Define features (X) and target (y)
X = data[['day_of_year', 'Tmin', 'Tmax', 'Prcp']]
y = data['Tavg']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))

# Predict today's and tomorrow's temperatures
def predict_temperature(model):
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    today_features = pd.DataFrame({
        'day_of_year': [today.timetuple().tm_yday],
        'Tmin': [X['Tmin'].iloc[-1]],
        'Tmax': [X['Tmax'].iloc[-1]],
        'Prcp': [X['Prcp'].iloc[-1]]
    })

    tomorrow_features = pd.DataFrame({
        'day_of_year': [tomorrow.timetuple().tm_yday],
        'Tmin': [X['Tmin'].iloc[-1]],
        'Tmax': [X['Tmax'].iloc[-1]],
        'Prcp': [X['Prcp'].iloc[-1]]
    })

    today_temp = model.predict(today_features)[0]
    tomorrow_temp = model.predict(tomorrow_features)[0]

    return today_temp, tomorrow_temp, tomorrow.date()

today_temp, tomorrow_temp, tomorrow_date = predict_temperature(model)

print(f"Predicted temperature for {tomorrow_date}: {tomorrow_temp:.2f}°C")
