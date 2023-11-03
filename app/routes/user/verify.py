from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models.user import User
from flask_login import login_user


@app.route('/verify', methods=['GET', 'POST'])
def verify_registration():
    if request.method == 'POST':
        email = request.form.get('email')
        code_entered = request.form.get('verification_code')

        # Check if the code entered matches the one stored in the session
        verification_code = session.get('verification_code')
        
        if verification_code and code_entered == verification_code:
            # Registration is successful, so add the user to the database
            first_name = session.get('first_name')
            last_name = session.get('last_name')
            password = session.get('password')
            email = session.get('email')
            
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            # code_entered = request.form.get('verification_code')
            # print(f"Code Entered: {code_entered}")

            user.generate_verification_code()
            db.session.add(user)
            db.session.commit()

            # Log in the user after registration
            login_user(user)
            
            # Clear the session data
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('password', None)
            session.pop('verification_code', None)

            flash('Verification successful. Account Created Succesfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')

    return render_template('user/verify.html')

