from app import app
from flask import render_template


#default error handler for invalid pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('root/error.html'), 404


# Custom error handler for internal server errors (HTTP status code 500)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('admin/internal_error.html'), 500
