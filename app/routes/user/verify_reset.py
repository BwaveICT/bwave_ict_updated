from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models.user import User
from app.models.user import User_PasswordReset

@app.route('/user/verify_reset/<reset_code>', methods=['GET', 'POST'])
def user_verify_reset(reset_code):
    # Check if the reset code exists in the UserPasswordReset table
    password_reset = User_PasswordReset.query.filter_by(reset_code=reset_code).first()

    if password_reset:
        if request.method == 'POST':
            # Change the user's password
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password == confirm_password:
                user = User.query.get(password_reset.user_id)
                user.set_password(new_password)
                db.session.delete(password_reset)
                db.session.commit()
                flash('Password reset successful. You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match. Please try again.', 'danger')
        return render_template("user/verify_reset.html", reset_code=reset_code)
    else:
        flash('Invalid or expired reset code.', 'danger')
        return redirect(url_for('user_reset_password'))
