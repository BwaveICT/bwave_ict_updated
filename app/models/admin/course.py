from app import db
from datetime import datetime
import locale

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    eligibility = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_start_date = db.Column(db.Date, nullable=False)
    deadline_date = db.Column(db.Date, nullable=False)


    def __init__(self, title, cost, eligibility, duration, slug, description, cover_photo, content, course_start_date, deadline_date):
        self.title = title
        self.cost = cost
        self.eligibility = eligibility
        self.duration = duration
        self.slug = slug
        self.description = description
        self.cover_photo = cover_photo
        self.content = content
        self.course_start_date = datetime.strptime(course_start_date, "%Y-%m-%d").date()
        self.deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date()


    def formatted_cost(self):
        # Set the locale to en_NG (Nigerian Naira)
        locale.setlocale(locale.LC_ALL, 'en_NG.UTF-8')
        
        # Format the cost as currency with NGN symbol, but without decimal places
        formatted_cost = locale.currency(self.cost, symbol=True, grouping=True)
        
        # Remove the decimal places if they exist
        if formatted_cost.endswith(".00"):
            formatted_cost = formatted_cost[:-3]

        return formatted_cost
