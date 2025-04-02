from datetime import datetime
from database import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords in production

    # Relationship to Expense (one-to-many)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the User table
    expense_amount = db.Column(db.Float, nullable=False)
    expense_type = db.Column(db.String(50), nullable=False)
    remaining_budget = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set the timestamp

    def __repr__(self):
        return f"<Expense(user_id={self.user_id}, amount={self.expense_amount}, type={self.expense_type}, remaining_budget={self.remaining_budget}, timestamp={self.timestamp})>"