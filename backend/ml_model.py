# ML Logic for Spending Prediction
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from models import Expense

def train_model():
    expenses = Expense.query.all()
    if len(expenses) < 3:
        return None  

    df = pd.DataFrame([(e.amount, e.date) for e in expenses], columns=['amount', 'date'])
    df['date'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)

    X = df[['date']]
    y = df['amount']

    model = LinearRegression()
    model.fit(X, y)

    future_date = pd.Timestamp.now().toordinal() + 30
    prediction = model.predict([[future_date]])[0]

    return prediction
