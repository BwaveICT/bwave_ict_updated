# routes/admin/reset_password.py
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models.admin import Admin
from app.models.admin import PasswordReset
import secrets
import os
from flask_mail import Message
from app import mail


@app.route('/admin/reset_password', methods=['GET', 'POST'])
def admin_reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        admin = Admin.query.filter_by(email=email).first()

        if admin:
            # Generate a unique reset code and save it in the PasswordReset table
            reset_code = generate_unique_reset_code() 
            password_reset = PasswordReset(admin_id=admin.id, reset_code=reset_code)
            db.session.add(password_reset)
            db.session.commit()

            # Send an email to the admin with the reset_code
            send_reset_email(admin.email, reset_code)  

            flash('A reset code has been sent to your email.', 'success')
            return redirect(url_for('admin_login'))
        else:
            flash('No admin found with that email.', 'danger')

    return render_template("admin/reset_password.html")


def generate_unique_reset_code():
    # Generate a secure and unique reset code
    reset_code = secrets.token_hex(16)
    return reset_code

def send_reset_email(recipient_email, reset_code):
    # Create a Message object with the email details
    message = Message('Password Reset', sender=os.environ.get('MAIL_USERNAME'), recipients=[recipient_email])

    message.html = render_template('admin/reset_password_email.html', reset_code=reset_code)

    mail.send(message)
