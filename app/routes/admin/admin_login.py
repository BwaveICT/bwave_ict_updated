from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models.admin import Admin

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'admin' in session:
        # Admin is already logged in, redirect to admin_dashboard
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if there are any admins in the admin DB
        admin_count = Admin.query.count()

        if admin_count == 0:
            # No admins in the DB, so the first user becomes the admin
            admin = Admin(email=email)
            admin.set_password(password)  # Set the password securely
            db.session.add(admin)
            db.session.commit()

            flash('You are now the admin. Welcome!', 'success')
            session['admin'] = True  # Set the admin session variable
            return redirect(url_for('admin_dashboard'))
        else:
            # Admins exist, so check the entered credentials
            admin = Admin.query.filter_by(email=email).first()
            if admin and admin.check_password(password):
                flash('Login successful!', 'success')
                session['admin'] = True  # Set the admin session variable
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid login details.', 'danger')

    return render_template("admin/admin-login.html")
