from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models.admin import Course
import os
from werkzeug.utils import secure_filename

@app.route('/admin/add_course', methods=['GET', 'POST'])
def add_course():
    if session.get('admin'):
        if request.method == 'POST':
            # Handle file upload
            file = request.files['cover_photo']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_photo_path = os.path.join('uploads', filename)  # Store the path in the database

            # Retrieve other form fields
            title = request.form.get('title')
            cost = float(request.form.get('cost'))
            eligibility = request.form.get('eligibility')
            duration = request.form.get('duration')
            slug = request.form.get('slug')
            description = request.form.get('description')
            course_start_date = request.form.get('course_start_date')
            deadline_date = request.form.get('deadline_date')
            content = request.form.get('content')

            # Create a new course object
            course = Course(title=title, cost=cost, eligibility=eligibility, duration=duration,
                            slug=slug, description=description, cover_photo=cover_photo_path, content=content, course_start_date=course_start_date, deadline_date=deadline_date)

            db.session.add(course)
            db.session.commit()

            flash('Course added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/add_course.html')
    else:
        flash('You are not logged in. No access to this page', 'danger')
        return redirect(url_for('admin_login'))


