from ..utils import db

class Courses(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=False)
    rating_total = db.Column(db.Float(), default=0)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'), nullable=False)
    instructor_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    category = db.relationship('Categories', backref='courses_list')
    instructor = db.relationship('Users', backref="courses_list")
    modules = db.relationship('Modules', backref='courses_list')
    enrollments = db.relationship('Enrollments', backref='courses_list')

    def __repr__(self):
        return f'<courses {self.title}>'