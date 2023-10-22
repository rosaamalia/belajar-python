from ..utils import db

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(256), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # one to many dengan Course
    courses = db.relationship('Courses', backref='categories')

    def __repr__(self):
        return f'<categories {self.category_name}>'