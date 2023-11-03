from flask import render_template, flash, redirect, url_for, session
from app import app

@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if the 'admin' session variable is set
    if session.get('admin'):
        return render_template("admin/dashboard.html")
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home_page'))  # Redirect to the index page
