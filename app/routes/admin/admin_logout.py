from app import app
from flask import redirect, url_for, session, flash

@app.route('/admin_logout')
def admin_logout():
    # Clear the 'admin' session variable
    session.pop('admin', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))
