from http import HTTPStatus

from . import db
from ..models.users import Users
from ..models.enrollments import Enrollments
from ..models.courses import Courses
from ..models.modules import Modules
from ..models.categories import Categories

# Cek id user ada atau tidak
def checkUserExist(user_id):
    user = Users.query.get(user_id)

    if(user):
        return True
    else:
        return False

# Cek role user
def checkUserRole(user_id, role):
    user = Users.query.get(user_id)
    user_role = user.role

    if(user_role == role):
        return True
    else:
        return False

# Cek user sudah terdaftar di course tersebut
def checkUserAlreadyEnrolled(user_id, course_id):
    enrollment = Enrollments.query.filter_by(user_id=user_id, course_id=course_id).first()

    if(enrollment):
        return True
    else:
        return False

# Cek course tersedia
def checkCourseExist(course_id):
    course = Courses.query.get(course_id)

    if(course):
        return True
    else:
        return False

# Cek kategori tersedia
def checkCategoryExist(category_id):
    category = Categories.query.get(category_id)

    if(category):
        return True
    else:
        return False

# Cek nama kategori sudah ada atau belum
def checkCategoryNameExist(category_name):
    category = Categories.query.filter_by(category_name=category_name).first()

    if(category):
        return True
    else:
        return False

# Cek title pada course sudah ada atau belum
def checkCourseTitleExist(course_title):
    course = Courses.query.filter_by(title=course_title).first()

    if(course):
        return True
    else:
        return False

# Update nilai total rating di course
def updateTotalRating(course_id):
    total_rating = Enrollments.query.with_entities(db.func.avg(Enrollments.rating)).filter_by(course_id=course_id).scalar()
    course = Courses.query.get(course_id)

    course.rating_total = total_rating
    db.session.commit()

    print(course.rating_total)