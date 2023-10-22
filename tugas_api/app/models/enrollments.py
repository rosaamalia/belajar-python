from ..utils import db

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    status = db.Column(db.Enum('ACTIVE', 'FINISH'), default='ACTIVE')
    rating = db.Column(db.Float(), default=0)
    review = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    user = db.relationship('Users', backref='enrollments_list')
    course = db.relationship('Courses', backref='enrollments_list')

    def __repr__(self):
        return f'<enrollments {self.user_id} - {self.course_id}>'