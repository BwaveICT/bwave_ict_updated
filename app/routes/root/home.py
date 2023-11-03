from flask import render_template
from app import app
from app.models.admin import Course 
from app.models.admin import  Blog

@app.route('/')
@app.route('/home')
def home_page():
    courses = Course.query.limit(3).all() 
    blogs = Blog.query.limit(5).all()
    return render_template("root/index.html", courses=courses, blogs=blogs)