from ..utils import db

class Modules(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    course = db.relationship('Courses', backref='modules_list')

    def __repr__(self):
        return f'<modules {self.title}>'