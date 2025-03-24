import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import os

# Load dataset
file_path = os.path.join(os.path.dirname(__file__), "personal_finance_dataset.csv")
df = pd.read_csv(file_path)

# Rename columns for easy access
df.columns = ["date", "mode", "category", "sub_category", "type", "amount"]

# Convert date column to proper format
df["date"] = pd.to_datetime(df["date"], format="%d %B %Y", errors="coerce")
df = df.dropna()  # Drop invalid rows

# Keep only expense rows
df = df[df["type"] == "Expense"]

# Convert amount column to numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna()  # Remove any non-numeric amounts

# Check if there are any expenses left
if df.empty:
    print("No expense data found after filtering!")
else:
    print(f"Total Expenses Used in ML: {len(df)}")

# Convert date to ordinal format (numerical values)
df["date_ordinal"] = df["date"].map(datetime.toordinal)

# Check if there are any expenses left
if df.empty:
    print("🚨 No expense data found after filtering! Check dataset formatting.")
else:
    print(f"✅ Total Expenses Used in ML: {len(df)}")
    print(df.head())  # Show first few rows


# Define features (X) and target (y)
X = df[["date_ordinal"]]  # Only using date as feature
y = df["amount"]  # Target is expense amount

# Split dataset into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)
# def train_model():
#     if df.empty:
#         print("🚨 No data available for ML training!")
#         return "No Data"  # Return this instead of None

#     future_date = [[datetime.now().toordinal() + 30]]  # Correct input format
#     avg_expense = np.mean(df["amount"])  # Use average expense if model fails

#     try:
#         prediction = model.predict([[future_date]])[0]  # Predict expense
#         return round(max(prediction, avg_expense), 2)  # Ensure valid prediction
#     except Exception as e:
#         print("🚨 ML Model Error:", e)
#         return round(avg_expense, 2)  # Use average expense if prediction fails

def train_model():
    future_date = np.array([[datetime.now().toordinal() + 30]])  # Convert to 2D array
    prediction = model.predict(future_date).item()
    return round(prediction, 2)
