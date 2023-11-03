from app import app
from flask import render_template

@app.route('/contact')
def contact_page():
    return render_template('root/contact.html')