from datetime import datetime
from app import db

class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.String(255), nullable=False)
    course_cost = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    expectation = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(255), nullable=True)  
    status = db.Column(db.String(10), default='pending', nullable=False)

    def __init__(self, course_id, course_name, start_date, course_cost, duration, first_name, last_name, email, country, state, phone_number, skills, payment_method, expectation, user_id, image_path=None):
        self.course_id = course_id
        self.course_name = course_name
        self.start_date = start_date
        self.course_cost = course_cost
        self.duration = duration
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.country = country
        self.state = state
        self.phone_number = phone_number
        self.skills = skills
        self.payment_method = payment_method
        self.expectation = expectation
        self.user_id = user_id
        self.image_path = image_path  
        self.status = 'pending'


