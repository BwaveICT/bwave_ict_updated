from app import db
from datetime import datetime

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    reset_code = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, admin_id, reset_code):
        self.admin_id = admin_id
        self.reset_code = reset_code
