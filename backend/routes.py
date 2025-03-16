from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import jwt
import datetime
from models import db, User, Expense
from ml_model import train_model

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Add Expense
@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(user_id=1, amount=data['amount'], category=data['category'], date=datetime.datetime.strptime(data['date'], "%Y-%m-%d"))
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

# Get Expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expense_list = [{'category': e.category, 'amount': e.amount, 'date': e.date.strftime('%Y-%m-%d')} for e in expenses]
    return jsonify(expense_list)

# Predict Future Spending
@app.route('/predict', methods=['GET'])
def predict():
    prediction = train_model()
    return jsonify({'predicted_spending': prediction}) if prediction else jsonify({'message': 'Not enough data to predict'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
