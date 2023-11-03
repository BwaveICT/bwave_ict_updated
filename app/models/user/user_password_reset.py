# models/user_password_reset.py
from app import db
from datetime import datetime

class User_PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    reset_code = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, reset_code):
        self.user_id = user_id
        self.reset_code = reset_code
