from flask import render_template
from app import app
from app.models.admin import Blog

@app.route('/blog/<string:slug>')
def blog(slug):
    # Query the blog post based on the slug
    blog = Blog.query.filter_by(slug=slug).first()
    recent_posts = Blog.query.order_by(Blog.date_posted.desc()).limit(5).all()
    return render_template('root/blog.html', blog=blog, recent_posts=recent_posts)
