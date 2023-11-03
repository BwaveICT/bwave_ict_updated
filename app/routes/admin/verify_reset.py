from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models.admin import Admin
from app.models.admin import PasswordReset

@app.route('/admin/verify_reset/<reset_code>', methods=['GET', 'POST'])
def admin_verify_reset(reset_code):
    # Check if the reset code exists in the PasswordReset table
    password_reset = PasswordReset.query.filter_by(reset_code=reset_code).first()

    if password_reset:
        if request.method == 'POST':
            # Change the admin's password
            new_password = request.form.get('new_password')
            admin = Admin.query.get(password_reset.admin_id)
            admin.set_password(new_password)
            db.session.delete(password_reset)
            db.session.commit()
            flash('Password reset successful. You can now log in.', 'success')
            return redirect(url_for('admin_login'))
        return render_template("admin/verify_reset.html", reset_code=reset_code)
    else:
        flash('Invalid or expired reset code.', 'danger')
        return redirect(url_for('admin_reset_password'))
