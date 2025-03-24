from flask import Flask
from models import db
import routes  # Import routes to register API endpoints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/as/financial-management-app/backend/expenses.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables when app starts
with app.app_context():
    db.create_all()

# Add a home route
@app.route('/')
def home():
    return "Welcome to the AI-Based Financial Management API!"

if __name__ == '__main__':
    app.run(debug=True)
