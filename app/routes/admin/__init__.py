from .admin_login import admin_login
from .admin_dashboard import admin_dashboard
from .admin_logout import admin_logout
from .add_course import add_course
from .edit_courses import edit_courses
from .edit_course import edit_course, delete_course
from .add_blog import add_blog,  allowed_file
from .edit_blogs import edit_blogs
from .tinymce_upload import tinymce_upload
from .edit_blog import edit_blog
from .reset_password import admin_reset_password, generate_unique_reset_code, send_reset_email
from .verify_reset import admin_verify_reset
from .view_applications import view_courses, view_applications, admin_view_application, send_email_to_applicant
