from flask import render_template, request
from app import app, db
from app.models.user import Applicant
from flask_login import login_required, current_user
from datetime import datetime

@app.route('/your_courses', methods=['GET'])
@login_required
def your_courses():
    # Get the selected status from the query string or default to 'all'
    selected_tab = request.args.get('status', 'all')

    # Fetch the courses applied for by the current user based on the selected status
    if selected_tab == 'all':
        courses = Applicant.query.filter_by(user_id=current_user.id).all()
    else:
        courses = Applicant.query.filter_by(user_id=current_user.id, status=selected_tab).all()

    # Convert the date_registered strings to datetime objects
    for course in courses:
        course.start_date = datetime.strptime(course.start_date, '%Y-%m-%d')

    return render_template('user/your_courses.html', courses=courses, selected_tab=selected_tab)
