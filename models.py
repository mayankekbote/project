from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # Import pytz for timezone handling

db = SQLAlchemy()

# Define IST timezone
ist = pytz.timezone('Asia/Kolkata')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # ⚠️ Plain-text passwords

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Name of the expense
    expense_amount = db.Column(db.Float, nullable=False)
    expense_type = db.Column(db.String(50), nullable=False)  # Type of expense
    remaining_budget = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(ist))  # Use IST timezone