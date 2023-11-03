from app import app
from flask import render_template
from app.models.admin import  Blog



@app.route('/blogs')
def blog_page():
    blogs = Blog.query.all()
    recent_posts = Blog.query.order_by(Blog.date_posted.desc()).limit(5).all()
    return render_template('root/blogs.html', blogs=blogs, recent_posts=recent_posts)