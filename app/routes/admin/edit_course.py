from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models.admin import Course
from werkzeug.utils import secure_filename
import os




@app.route('/admin/edit_course/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if session.get('admin'):
        course = Course.query.get(id)
        if not course:
            flash('Course not found', 'danger')
            return redirect(url_for('edit_courses'))
        
        if request.method == 'POST':
            course.title = request.form.get('title')
            course.cost = float(request.form.get('cost'))
            course.eligibility = request.form.get('eligibility')
            course.duration = request.form.get('duration')
            course.slug = request.form.get('slug')
            course.description = request.form.get('description')
            course.course_start_date = request.form.get('course_start_date')
            course.deadline_date = request.form.get('deadline_date')
            course.content = request.form.get('content')

            # Check if a new cover photo was uploaded
            new_cover_photo = request.files.get('cover_photo')
            if new_cover_photo:
                cover_photo_filename = secure_filename(new_cover_photo.filename)
                new_cover_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_photo_filename))
                course.cover_photo = os.path.join('uploads', cover_photo_filename)

            db.session.commit()

            flash('Course updated successfully!', 'success')
            return redirect(url_for('edit_courses'))

        return render_template('admin/edit_course.html', course=course)
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
    



# Delete the course.


@app.route('/admin/delete_course/<int:id>', methods=['GET'])
def delete_course(id):
    if session.get('admin'):
        course = Course.query.get(id)
        if not course:
            flash('Course not found', 'danger')
            return redirect(url_for('edit_courses'))

        db.session.delete(course)
        db.session.commit()

        flash('Course deleted successfully!', 'success')
        return redirect(url_for('edit_courses'))
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
