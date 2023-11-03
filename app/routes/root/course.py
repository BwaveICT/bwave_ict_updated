from app import app
from flask import render_template
from app.models.admin import Course
from datetime import datetime

@app.route('/course/<slug>')
def course(slug):
    # Query the database for the course with the provided slug
    course = Course.query.filter_by(slug=slug).first()
    current_date = datetime.now()
    return render_template('root/course.html', course=course, current_date=current_date)

