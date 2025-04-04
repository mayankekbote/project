from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Expense
from datetime import datetime
import pytz  # Import pytz for timezone handling

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False  # Optional: Keeps sessions temporary

db = SQLAlchemy(app)

# User Model (Storing passwords as plain text - Not recommended for real-world use)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # ⚠️ Plain-text passwords


# Define IST timezone
ist = pytz.timezone('Asia/Kolkata')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expense_amount = db.Column(db.Float, nullable=False)
    expense_type = db.Column(db.String(50), nullable=False)
    remaining_budget = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(ist))  # Use IST timezone

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"status": "error", "message": "Username and password are required!"}), 400

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({"status": "error", "message": "Username already exists!"}), 409

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"status": "success", "message": "Registration successful!"}), 201
        
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred while processing your request."}), 500


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            # Check if user exists in database
            user = User.query.filter_by(username=username).first()

            if user and user.password == password:  # ⚠️ Plain-text password check (No hashing)
                session["user_id"] = user.id
                return jsonify({"status": "success", "message": "Login successful!"}), 200
            else:
                return jsonify({"status": "error", "message": "Incorrect username or password!"}), 401

        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred while processing your request."}), 500

# Dashboard Route (Requires Login)
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template('dashboard.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "User not logged in!"}), 401

    try:
        data = request.get_json()
        expense_amount = data.get("expense_amount")
        expense_type = data.get("expense_type")
        remaining_budget = data.get("remaining_budget")

        # Validate input
        if not expense_amount or not expense_type or remaining_budget is None:
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Create a new Expense record
        new_expense = Expense(
            user_id=session["user_id"],
            expense_amount=expense_amount,
            expense_type=expense_type,
            remaining_budget=remaining_budget
        )

        # Add and commit to the database
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({"status": "success", "message": "Expense added successfully!"}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": "An error occurred while processing your request."}), 500 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist


    app.run(debug=True)
