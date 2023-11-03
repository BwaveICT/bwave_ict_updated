from app import app
from flask import render_template

@app.route('/services')
def services_page():
    return render_template('root/services.html')


@app.route('/website_development')
def website_page():
    return render_template('root/web-dev.html')


@app.route('/app_development')
def app_page():
    return render_template('root/app-dev.html')




