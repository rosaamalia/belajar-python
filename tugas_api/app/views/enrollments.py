from http import HTTPStatus
from flask import request, jsonify, current_app, Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utils import db
from ..utils.utils import checkAuthenticated, checkUserExist, checkUserRole, checkCourseExist, checkUserAlreadyEnrolled, updateTotalRating
from ..logs.log import logger
from ..models.enrollments import Enrollments

enrollments_ns = Namespace('enrollments', description='Namespace for enrollments')

enrollments_input_model = enrollments_ns.model(
    'EnrollmentInput', {
        'user_id': fields.Integer(description='User ID', required=True),
        'course_id': fields.Integer(description='enrollment ID', required=True),
        'status': fields.String(description='Status', enum=['ACTIVE', 'FINISH'], required=True),
        'rating': fields.Float(description='Rating', nullable=True),
        'review': fields.String(description='Review', nullable=True),
    }
)

enrollments_output_model = enrollments_ns.model(
    'Enrollment', {
        'id': fields.Integer(),
        'user_id': fields.Integer(),
        'course_id': fields.Integer(),
        'status': fields.String(),
        'rating': fields.Float(),
        'review': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

@enrollments_ns.route('/')
class EnrollmentResource(Resource):
    @enrollments_ns.expect(enrollments_input_model)
    @enrollments_ns.marshal_with(enrollments_output_model)
    @enrollments_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def post(self):
        """Create a new enrollment"""
        data = enrollments_ns.payload
        user_id = data.get('user_id')
        course_id = data.get('course_id')

        # Cek user ada atau tidak
        if(checkUserExist(user_id) is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH ID {user_id} IS NOT FOUND")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="User is not found.")

        # Cek role user
        if(checkUserRole(user_id, 'STUDENT') is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH ID {user_id} IS NOT A STUDENT")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="User is not a student.")

        # Cek course tersedia
        if(checkCourseExist(course_id) is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - COURSE WITH ID {course_id} IS NOT FOUND")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="Course is not found.")

        # Cek user sudah terdaftar atau belum
        if(checkUserAlreadyEnrolled(user_id, course_id) is True):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH ID {user_id} IS ALREADY ENROLLED COURSE WITH ID {course_id}")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="User is already enrolled.")

        # Cek nilai rating di antara 0 sampai 5
        if(data.get('rating') > 5 or data.get('rating') < 0):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - RATING IS NOT IN THE RANGE OF O TO 5")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="Rating value must be in the range of 0 to 5.")

        enrollment = Enrollments(**data)  # Membuat objek enrollment dari payload
        db.session.add(enrollment)
        db.session.commit()

        # Update nilai rating total di course
        updateTotalRating(course_id)
        logger.info(f"POST ENROLLMENT DATA WITH ID {enrollment.id}")

        return enrollment, 201

@enrollments_ns.route('/<int:enrollment_id>')
class EnrollmentById(Resource):
    @enrollments_ns.doc(description = "Get enrollment data by id", params = {"enrollment_id": "Id enrollment"})
    @enrollments_ns.marshal_list_with(enrollments_output_model)
    @enrollments_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self, enrollment_id):
        """Get enrollment data by id"""
        try:
            data = Enrollments.query.get_or_404(enrollment_id)
            logger.info(f"GET ENROLLMENT DATA WITH ID {data.id}")
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @enrollments_ns.doc(description = "Edit enrollment data by id", params = {"enrollment_id": "Id enrollment"})
    @enrollments_ns.expect(enrollments_input_model)
    @enrollments_ns.marshal_with(enrollments_input_model)
    @enrollments_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def put(self, enrollment_id):
        """Edit enrollment data"""
        data_from_database = Enrollments.query.get_or_404(enrollment_id)
        data = request.get_json(force=True)

        email = get_jwt_identity()
        if(checkAuthenticated(data_from_database.user_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO EDIT ENROLLMENT DATA WITH ID {enrollment_id}")
            enrollments_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        # Cek nilai rating di antara 0 sampai 5
        if(data['rating'] > 5 or data['rating'] < 0):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - RATING IS NOT IN THE RANGE OF O TO 5")
            enrollments_ns.abort(HTTPStatus.BAD_REQUEST, message="Rating value must be in the range of 0 to 5.")

        data_from_database.user_id = data['user_id']
        data_from_database.course_id = data['course_id']
        data_from_database.status = data['status']
        data_from_database.rating = data['rating']
        data_from_database.review = data['review']

        db.session.commit()
        updateTotalRating(data['course_id'])

        logger.info(f"EDIT ENROLLMENT DATA WITH ID {data_from_database.id}")
        return data_from_database, HTTPStatus.OK
    
    @enrollments_ns.doc(description = "Delete enrollment data by id", params = {"enrollment_id": "Id enrollment"})
    @enrollments_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def delete(self, enrollment_id):
        """Delete enrollment data"""
        data = Enrollments.query.get_or_404(enrollment_id)

        email = get_jwt_identity()
        if(checkAuthenticated(data.user_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO DELETE ENROLLMENT DATA WITH ID {enrollment_id}")
            enrollments_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        db.session.delete(data)
        db.session.commit()

        logger.info(f"DELETE ENROLLMENT DATA WITH ID {data.id}")
        return {'message': "Data is succesfully deleted."}, HTTPStatus.OK