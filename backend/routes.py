from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import jwt
import datetime
from models import db, User, Expense
import os

# Import ML model safely
try:
    from ml_model import train_model
except ImportError:
    train_model = None

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/as/financial-management-app/backend/expenses.db'
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
print("✅ Flask connected to database:", app.config['SQLALCHEMY_DATABASE_URI'])



# ✅ DEBUG: Forcefully Drop & Recreate Tables
with app.app_context():
    # print("🚀 Dropping existing tables (if any)...")
    # db.drop_all()  # Remove this line later
    db.create_all()
    db.session.commit()  # ✅ Force commit the changes
    print("✅ Tables created successfully!")
    db_path = os.path.abspath("expenses.db")
    print(f"✅ Database location: {db_path}")


# Register User
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Missing username or password"}), 400

        # Check if username already exists
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return jsonify({"error": "Username already taken"}), 409  # 409 Conflict

        hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        new_user = User(username=data["username"], password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Missing username or password"}), 400

        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            return jsonify({"error": "User not found"}), 401

        # Convert both to bytes before checking
        if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
            token = jwt.encode(
                {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
                app.config["SECRET_KEY"], algorithm="HS256"
            )
            return jsonify({"token": token})

        return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# # ✅ Add Expense (User Must Exist)
# @app.route('/expense', methods=['POST'])
# def add_expense():
#     try:
#         data = request.json
#         if not all(k in data for k in ("amount", "category", "date")):
#             return jsonify({'error': 'Missing required fields'}), 400

#         # Ensure user exists (Currently assuming user_id = 1 for testing)
#         from sqlalchemy.orm import Session
#         with Session(db.engine) as session:
#           user = session.get(User, 1)

#         # Remove user check or handle it differently
#         user = User.query.get(1)
#         if not user:
#             user = User(id=1, username="Madhu", password="XYZ")
#             db.session.add(user)
#             db.session.commit()
#             print("✅ Default user created")

@app.route('/expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        user = User.query.get(1)  # Fix for missing user
        
        if not user:
            return jsonify({"error": "User not found"}), 400

        new_expense = Expense(
            user_id=user.id,
            amount=float(data["amount"]),
            category=data["category"],
            date=datetime.datetime.strptime(data["date"], "%Y-%m-%d"),
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"message": "Expense added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



        new_expense = Expense(
            user_id = user.id,
            amount=data['amount'], 
            category=data['category'], 
            date=datetime.datetime.strptime(data['date'], "%Y-%m-%d")
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'message': 'Expense added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Get Expenses (Retrieve All)
@app.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        expenses = Expense.query.all()
        if not expenses:
            return jsonify([])  # Return an empty list instead of an error

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

print("✅ Available Routes in Flask:")
for rule in app.url_map.iter_rules():
    print(rule)


if __name__ == '__main__':
    app.run(debug=True)
