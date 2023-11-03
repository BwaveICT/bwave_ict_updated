from flask import render_template, redirect, url_for, flash, session, request
from app import app, db
from app.models.admin import Blog
from werkzeug.utils import secure_filename
from .add_blog import allowed_file
import os

@app.route('/admin/edit_blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    if session.get('admin'):
        blog = Blog.query.get(id)
        if not blog:
            flash('Blog post not found', 'danger')
            return redirect(url_for('edit_blogs'))

        if request.method == 'POST':
            title = request.form.get('title')
            author = request.form.get('author')
            date_posted = request.form.get('date_posted')
            slug = request.form.get('slug')
            duration = request.form.get('duration')
            cover_photo_file = request.files['cover_photo']
            categories = request.form.get('categories')
            description = request.form.get('description')
            content = request.form.get('content')

            if cover_photo_file and allowed_file(cover_photo_file.filename):
                filename = secure_filename(cover_photo_file.filename)
                cover_photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_photo = filename
                blog.cover_photo = cover_photo

            blog.title = title
            blog.author = author
            blog.date_posted = date_posted
            blog.slug = slug
            blog.duration = duration
            blog.categories = categories
            blog.description = description
            blog.content = content

            db.session.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('edit_blogs'))

        return render_template('admin/edit_blog.html', blog=blog)
    else:
        flash('You are not logged in. No access to this page', 'danger')
        return redirect(url_for('admin_login'))



@app.route('/admin/delete_blog/<int:id>')
def delete_blog(id):
    if session.get('admin'):
        blog = Blog.query.get(id)
        if not blog:
            flash('Blog post not found', 'danger')
            return redirect(url_for('edit_blogs'))

        db.session.delete(blog)
        db.session.commit()
        flash('Blog post deleted successfully!', 'success')
        return redirect(url_for('edit_blogs'))
    else:
        flash('You are not logged in. No access to this page', 'danger')
        return redirect(url_for('admin_login'))
