from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager  
from flask_session import Session  
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Load environment variables from .env file
load_dotenv()

# Load secret key from environment variable
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Load database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)


# db migration
migrate = Migrate(app, db)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")



app.config['UPLOAD_FOLDER'] = 'app/static/uploads'  



# Initialize Flask-Mail for sending emails
mail = Mail(app)


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'admin_login'  # Use the name of your admin login route
login_manager.login_message_category = 'info'
login_manager.init_app(app)
# Session(app)

# User loader for regular users
@login_manager.user_loader
def load_user(user_id):
    # Import the User model here to avoid circular import
    from app.models.user import User
    return User.query.get(int(user_id))

# User loader for admin users
@login_manager.request_loader
def load_admin(request):
    if request.endpoint == 'admin_login' and request.method == 'POST':
        # Load the admin user here
        from app.models.admin import Admin
        admin_id = request.form.get('admin_id')  # You might need to adapt this to your form
        return Admin.query.get(int(admin_id))





# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

from app.routes.root import *
from app.routes.admin import *
from app.routes.user import *

if __name__ == '__main__':
    app.run()
