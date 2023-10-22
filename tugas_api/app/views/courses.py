from http import HTTPStatus
from flask import request, jsonify, current_app, Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utils import db
from ..utils.utils import checkAuthenticated, checkCourseTitleExist, checkCategoryExist, checkUserExist, checkUserRole
from ..logs.log import logger
from ..models.courses import Courses

courses_ns = Namespace('courses', description='Namespace for courses')

courses_input_model = courses_ns.model(
    'CoursesInput', {
        'title': fields.String(),
        'description': fields.String(),
        'category_id': fields.Integer(),
        'instructor_id': fields.Integer()
    }
)

categories_model = courses_ns.model(
    'Categories', {
        'id': fields.Integer(),
        'category_name': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

users_model = courses_ns.model(
    'Users', {
        'id': fields.Integer(),
        'email': fields.String(),
        'role': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

modules_model = courses_ns.model(
    'Modules', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'content': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

enrollments_model = courses_ns.model(
    'Enrollments', {
        'id': fields.Integer(),
        'course_id': fields.Integer(),
        'user': fields.Nested(users_model),
        'status': fields.String(),
        'rating': fields.Float(),
        'review': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

courses_get_model = courses_ns.model(
    'Courses', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'rating_total': fields.Float(),
        'category': fields.Nested(categories_model),
        'instructor': fields.Nested(users_model),
        'created_at': fields.String(),
        'updated_at': fields.String(),
        'modules': fields.List(fields.Nested(modules_model)),
        'enrollments': fields.List(fields.Nested(enrollments_model))
    }
)

@courses_ns.route('/')
class CourseGetPost(Resource):
    @courses_ns.marshal_list_with(courses_get_model)
    @courses_ns.doc(description = "Get all courses")
    @courses_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self):
        """Get all courses"""
        try:
            data = Courses.query.all()
            logger.info(f"GET ALL CATEGORY DATA")
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @courses_ns.doc(description = "Create new course data")
    @courses_ns.expect(courses_input_model)
    @courses_ns.marshal_with(courses_input_model)
    @courses_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def post(self):
        """Create new course data"""
        # data = courses_ns.payload # bisa pakai ini juga
        data = courses_ns.payload
        user_id = data.get('instructor_id')
        print(data)

        # Cek title sudah ada atau belum
        if(checkCourseTitleExist(data.get('title')) is True):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - COURSE WITH TITLE {data.get('title')} IS ALREADY EXIST")
            courses_ns.abort(HTTPStatus.BAD_REQUEST, message="Title is already exist.")

        # Cek kategori ada
        if(checkCategoryExist(data.get('category_id')) is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - CATEGORY WITH ID {data.get('category_id')} IS NOT FOUND")
            courses_ns.abort(HTTPStatus.BAD_REQUEST, message="Category is not found.")
        
        # Cek instruktur ada atau tidak
        if(checkUserExist(user_id) is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH ID {data.get('user_id')} IS NOT FOUND")
            courses_ns.abort(HTTPStatus.BAD_REQUEST, message="User is not found.")
        
        # Cek role user
        if(checkUserRole(user_id, 'INSTRUCTOR') is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH ID {data.get('user_id')} IS NOT A INSTRUCTOR")
            courses_ns.abort(HTTPStatus.BAD_REQUEST, message="User is not a instructor.")

        input = Courses(
            title = data.get('title'),
            description = data.get('description'),
            category_id = data.get('category_id'),
            instructor_id = data.get('instructor_id'),
        )

        print(input)
        db.session.add(input)
        db.session.commit()

        logger.info(f"POST COURSE DATA WITH ID {input.id}")
        return input, HTTPStatus.CREATED
        
@courses_ns.route('/<int:course_id>')
class CourseById(Resource):
    @courses_ns.doc(description = "Get course data by id", params = {"course_id": "Id course"})
    @courses_ns.marshal_list_with(courses_get_model)
    @courses_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self, course_id):
        """Get course data by id"""
        try:
            data = Courses.query.get_or_404(course_id)
            logger.info(f"GET COURSE DATA WITH ID {data.id}")
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @courses_ns.doc(description = "Edit course data by id", params = {"course_id": "Id course"})
    @courses_ns.expect(courses_input_model)
    @courses_ns.marshal_with(courses_input_model)
    @courses_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def put(self, course_id):
        """Edit course data"""
        data_from_database = Courses.query.get_or_404(course_id)
        data = request.get_json(force=True)

        email = get_jwt_identity()
        if(checkAuthenticated(data_from_database.instructor_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO EDIT COURSE DATA WITH ID {course_id}")
            courses_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        data_from_database.title = data['title']
        data_from_database.description = data['description']
        data_from_database.rating_total = data['rating_total']
        data_from_database.category_id = data['category_id']
        data_from_database.instructor_id = data['instructor_id']

        db.session.commit()

        logger.info(f"PUT COURSE DATA WITH ID {data_from_database.id}")
        return data_from_database, HTTPStatus.OK
    
    @courses_ns.doc(description = "Delete course data by id", params = {"course_id": "Id course"})
    @courses_ns.marshal_with(courses_input_model)
    @courses_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def delete(self, course_id):
        """Delete course data"""
        data = Courses.query.get_or_404(course_id)

        email = get_jwt_identity()
        if(checkAuthenticated(data.instructor_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO DELETE COURSE DATA WITH ID {course_id}")
            courses_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        db.session.delete(data)
        db.session.commit()

        logger.info(f"DELETE COURSE DATA WITH ID {data.id}")
        return {'message': "Data is succesfully deleted."}, HTTPStatus.OK