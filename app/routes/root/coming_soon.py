from app import app
from flask import render_template

@app.route('/coming_soon')
def coming_soon():
    return render_template('root/soon.html')