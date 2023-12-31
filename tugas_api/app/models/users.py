from ..utils import db

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('STUDENT', 'INSTRUCTOR'), nullable=False, default='STUDENT')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    enrollments = db.relationship('Enrollments', backref='users')

    def __repr__(self):
        return f'<users {self.email} - {self.role}>'