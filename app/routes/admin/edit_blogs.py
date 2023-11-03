from flask import render_template, redirect, url_for, flash, session
from app import app, db
from app.models.admin import Blog

@app.route('/admin/edit_blogs', methods=['GET'])
def edit_blogs():
    if session.get('admin'):
        # Retrieve a list of existing blog posts
        blogs = Blog.query.all()
        return render_template('admin/edit_blogs.html', blogs=blogs)
    else:
        flash('You are not logged in. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
