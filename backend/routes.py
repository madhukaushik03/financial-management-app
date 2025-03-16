from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import jwt
import datetime
from models import db, User, Expense

# Import ML model safely
try:
    from ml_model import train_model
except ImportError:
    train_model = None

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Ensure database tables are created
with app.app_context():
    db.create_all()

# ✅ Register User
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ User Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data['username']).first()

        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
                               app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})

        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Add Expense
@app.route('/expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        new_expense = Expense(
            user_id=1,  
            amount=data['amount'], 
            category=data['category'], 
            date=datetime.datetime.strptime(data['date'], "%Y-%m-%d")
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'message': 'Expense added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Get Expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        expenses = Expense.query.all()
        expense_list = [{'category': e.category, 'amount': e.amount, 'date': e.date.strftime('%Y-%m-%d')} for e in expenses]
        return jsonify(expense_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Predict Future Spending (AI)
@app.route('/predict', methods=['GET'])
def predict():
    if train_model is None:
        return jsonify({'error': 'ML model is not available'}), 500

    try:
        prediction = train_model()
        if prediction:
            return jsonify({'predicted_spending': prediction})
        else:
            return jsonify({'message': 'Not enough data to predict'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AI-Based Financial Management API!'})

if __name__ == '__main__':
    app.run(debug=True)
