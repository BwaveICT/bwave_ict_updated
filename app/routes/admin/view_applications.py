from flask import render_template, redirect, request, flash, url_for, session
from flask_login import login_required
from app import app, db, mail
from app.models.admin import Course
from app.models.user import Applicant
from flask_mail import Message


@app.route('/admin/view_courses')
def view_courses():
    if session.get('admin'):
        # Retrieve a list of courses from the database
        courses = Course.query.all()
        return render_template('admin/view_courses.html', courses=courses)
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/admin/view_applications/<int:course_id>')
def view_applications(course_id):
    if session.get('admin'):
        # Retrieve a list of applications for the selected course
        course = Course.query.get(course_id)
        applications = Applicant.query.filter_by(course_id=course_id).all()
        return render_template('admin/view_applications.html', course=course, applications=applications)
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))



@app.route('/admin/view_application/<int:applicant_id>', methods=['GET', 'POST'])
def admin_view_application(applicant_id):
    if session.get('admin'):
        
        # Fetch the applicant's data from the database based on the applicant_id
        applicant = Applicant.query.get_or_404(applicant_id)

    

        if request.method == 'POST':
        # Get the admin's action from the form
            admin_action = request.form.get('admin-action')

            if applicant.status in ['approved', 'rejected']:
                flash('The status of this application has already been updated and cannot be changed.', 'danger')
                return redirect(url_for('admin_dashboard'))

        # Handle the admin's decision, such as updating the status in the database
            if admin_action == 'accept':
                applicant.status = 'approved'
                db.session.commit()
                send_email_to_applicant(applicant, 'Congratulations! Welcome To Bwave ICT', 'user/  application_approved_mail.html')
            elif admin_action == 'reject':
                # Delete the application and its associated data from the database
                db.session.delete(applicant)
                db.session.commit()
                send_email_to_applicant(applicant, 'Application Rejected', 'user/application_rejected_mail.html')
                flash('Application has been rejected and deleted.', 'success')
                return redirect(url_for('admin_dashboard'))

            # You can also perform additional actions, such as sending notifications

            flash('Application status updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/view_application.html', applicant=applicant)
    
    else:
        flash('You are not logged in as an admin. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
        



def send_email_to_applicant(applicant, subject, template):
    recipients = [applicant.email]
    message = Message(subject=subject, recipients=recipients)
    message.html = render_template(template, applicant=applicant)

    try:
        mail.send(message)
        flash(f'Email notification sent to {applicant.first_name}', 'success')
    except Exception as e:
        flash('Failed to send email notification. Please check your email settings.', 'danger')
        app.logger.error(str(e))
