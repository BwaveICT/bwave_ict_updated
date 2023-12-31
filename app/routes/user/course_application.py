from flask import request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import app, db, mail
from app.models.admin import Course
from app.models.user import Applicant
import os
from werkzeug.utils import secure_filename
from flask_mail import Message

@app.route('/apply_for_course/<slug>', methods=['GET', 'POST'])
@login_required
def apply_for_course(slug):
    course = Course.query.filter_by(slug=slug).first()
    user_id = current_user.id

    existing_application = Applicant.query.filter_by(user_id=user_id, course_id=course.id).first()

    if existing_application:
        flash('You have already applied for this course. Multiple applications are not allowed.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Get form data
        course_name = course.title
        start_date = course.course_start_date
        course_cost = course.cost
        duration = course.duration
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = current_user.email
        country = request.form.get('country')
        state = request.form.get('state')
        phone_number = request.form.get('phone_number')
        skills = request.form.get('skills')
        payment_method = request.form.get('payment_method')
        expectation = request.form.get('expectation')

        # Check for missing values
        if not all([first_name, last_name, country, state, phone_number, skills, payment_method, expectation]):
            flash('Please fill out all the required fields', 'danger')
            return redirect(request.url)  # Redirect back to the form

        # Handle file upload
        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            # Save the uploaded file to the upload folder
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Store the image path in the database
            image_path = os.path.join('uploads', filename)
        else:
            image_path = None

        # Store other information in the database
        applicant = Applicant(
            course_id=course.id,
            course_name=course_name,
            start_date=start_date,
            course_cost=course_cost,
            duration=duration,
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            state=state,
            phone_number=phone_number,
            skills=skills,
            payment_method=payment_method,
            expectation=expectation,
            user_id=current_user.id,
            image_path=image_path
        )

        db.session.add(applicant)
        db.session.commit()

        send_email_to_user(applicant)

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('user/course_application.html', course=course)


def send_email_to_user(applicant):
    subject = 'Application Received and Under Review'
    recipients = [applicant.email]
    message = Message(subject=subject, recipients=recipients)

    # Render the HTML template for the email body
    email_body = render_template('user/application_received_mail.html', applicant=applicant)
    message.html = email_body

    try:
        mail.send(message)
        flash('An Email has been sent to you', 'success')
    except Exception as e:
        flash('Failed to send email notification. Please check your email settings.', 'danger')
        app.logger.error(str(e))

