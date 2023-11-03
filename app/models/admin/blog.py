from app import db
from sqlalchemy.orm import relationship

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

    def __init__(self, text):
        self.text = text

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)

    # Use a relationship for comments
    comments = relationship("Comment", backref="blog")

    categories = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, author, date_posted, slug, duration, cover_photo, categories, description, content):
        self.title = title
        self.author = author
        self.date_posted = date_posted
        self.slug = slug
        self.duration = duration
        self.cover_photo = cover_photo

        self.categories = categories
        self.description = description
        self.content = content

    def add_comment(self, comment):
        # Add a comment to the blog
        self.comments.append(comment)
