from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from app.models.admin import Blog, Comment
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'app/static/uploads/'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/admin/add_blog', methods=['GET', 'POST'])
def add_blog():
    if session.get('admin'):
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
                # Securely save the uploaded file
                filename = secure_filename(cover_photo_file.filename)
                cover_photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_photo = filename
            else:
                cover_photo = None


            # Create a new blog post with default comments count of 0
            blog = Blog(
                title=title, author=author, date_posted=date_posted, slug=slug, duration=duration,
                cover_photo=cover_photo, categories=categories,
                description=description, content=content
            )
            db.session.add(blog)
            db.session.commit()

            flash('Blog post added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/add_blog.html')
    else:
        flash('You are not logged in. No access to this page', 'danger')
        return redirect(url_for('admin_login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
