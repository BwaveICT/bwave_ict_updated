from app import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random
from flask_login import UserMixin
from app.models.user.applicant import Applicant


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    verification_code = db.Column(db.String(6))
    verification_code_created_at = db.Column(db.DateTime)
    registered_at = db.Column(db.DateTime, server_default=func.now())
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin  # Set the admin status during user creation

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_code_created_at = datetime.datetime.utcnow()

    def verify_code(self, code):
        if self.verification_code == code and self.is_code_valid():
            self.verification_code = None
            self.verification_code_created_at = None
            return True
        return False

    def is_code_valid(self):
        if not self.verification_code_created_at:
            return False
        time_difference = datetime.datetime.utcnow() - self.verification_code_created_at
        return time_difference.total_seconds() <= 600

    def has_applied_for_course(self, course):
        # Check if the user has already applied for the given course
        return Applicant.query.filter_by(user_id=self.id, course_id=course.id).first() is not None