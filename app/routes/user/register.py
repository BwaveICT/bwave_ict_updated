from flask import render_template, request, redirect, url_for, flash, session
import random
from app import app, db
from app.models.user import User
from flask_mail import Message
from app import mail


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            # Generate a verification code and store it in the session
            verification_code = str(random.randint(100000, 999999))
            session['verification_code'] = verification_code
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['password'] = password
            session['email'] = email

            # Send verification email to the user
            send_verification_email(email, verification_code, first_name)

            flash('One More Step. Check your email for a verification code.', 'success')
            return redirect(url_for('verify_registration'))

    return render_template('root/register.html')




def send_verification_email(to_email, verification_code, first_name):
    subject = 'Verification Code for Your Registration'
    html_body = render_template('user/verify_email.html', verification_code=verification_code, first_name=first_name)
    msg = Message(subject, recipients=[to_email], html=html_body)
    mail.send(msg)
