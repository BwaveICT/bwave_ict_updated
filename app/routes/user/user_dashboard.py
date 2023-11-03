from app import app, db
from flask import render_template
from flask_login import login_required, current_user
from app.models.admin import Course
from app.models.user import Applicant

@app.route('/dashboard')
@login_required
def dashboard():
    # Get the count of available courses
    available_courses_count = Course.query.count()

    # Get the count of courses the user has applied for
    user_id = current_user.id
    user_applied_courses_count = Applicant.query.filter_by(user_id=user_id).count()

    return render_template("user/dashboard.html", available_courses_count=available_courses_count, user_applied_courses_count=user_applied_courses_count)
