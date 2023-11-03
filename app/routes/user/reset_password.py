from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.models.user import User
from app.models.user import User_PasswordReset
import secrets
from flask_mail import Message
from app import mail
import os


@app.route('/user/reset_password', methods=['GET', 'POST'])
def user_reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a unique reset code and save it in the PasswordReset table
            reset_code = generate_unique_reset_code() 
            password_reset = User_PasswordReset(user_id=user.id, reset_code=reset_code)
            db.session.add(password_reset)
            db.session.commit()

            # Send an email to the user with the reset_code
            send_user_reset_email(user.email, reset_code)  
            flash('A reset code has been sent to your email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('No user found with that email.', 'danger')

    return render_template("user/reset_password.html")




def generate_unique_reset_code():
    # Generate a secure and unique reset code
    reset_code = secrets.token_hex(16)
    return reset_code

def send_user_reset_email(recipient_email, reset_code):
    # Create a Message object with the email details
    message = Message('Password Reset', sender=os.environ.get('MAIL_USERNAME'), recipients=[recipient_email])

    message.html = render_template('user/reset_password_email.html', reset_code=reset_code)

    mail.send(message)
