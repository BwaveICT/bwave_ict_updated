from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models.admin import Course


@app.route('/admin/edit_courses', methods=['GET'])
def edit_courses():
    if session.get('admin'):
        # Query all courses from the database
        courses = Course.query.all()
        return render_template('admin/edit_courses.html', courses=courses)
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
