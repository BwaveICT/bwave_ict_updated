from flask import session, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from app import app

@app.route('/logout')
@login_required  # Requires users to be logged in to access this route
def logout():
    logout_user()
    
    # Clear user details from session
    session.pop('user_id', None)
    session.pop('user_email', None)

    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
