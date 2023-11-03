from app import app
from app.models.admin import Course 
from flask import render_template, request



@app.route('/courses')
def courses_page():
    per_page = 6
    page = request.args.get('page', 1, type=int)
    courses = Course.query.paginate(page=page, per_page=per_page)
    return render_template("root/courses.html", courses=courses)