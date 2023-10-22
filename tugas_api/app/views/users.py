from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utils import db
from ..utils.utils import checkAuthenticated
from ..logs.log import logger
from ..models.users import Users

users_ns = Namespace('users', description='Namespace for users')

users_input_model = users_ns.model(
    'UsersInput', {
        'email': fields.String(),
        'password': fields.String(),
        'role': fields.String(),
    }
)

categories_model = users_ns.model(
    'Categories', {
        'id': fields.Integer(),
        'category_name': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

users_model = users_ns.model(
    'Users', {
        'id': fields.Integer(),
        'email': fields.String(),
        'role': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

courses_model = users_ns.model(
    'Courses', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'rating_total': fields.Float(),
        'category': fields.Nested(categories_model),
        'instructor': fields.Nested(users_model),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

enrollments_model = users_ns.model(
    'Enrollments', {
        'id': fields.Integer(),
        'user_id': fields.Integer(),
        'course': fields.Nested(courses_model),
        'status': fields.String(),
        'rating': fields.Float(),
        'review': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

users_output_model = users_ns.model(
    'UsersOutput', {
        'id': fields.Integer(),
        'email': fields.String(),
        'role': fields.String(),
        'enrollments': fields.List(fields.Nested(enrollments_model)),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

@users_ns.route('/')
class UserGetPost(Resource):
    @users_ns.marshal_list_with(users_output_model)
    @users_ns.doc(description = "Get all users")
    @users_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self):
        """Get all users"""
        try:
            data = Users.query.all()

            logger.info('GET ALL USERS DATA')
            return data, HTTPStatus.OK
        except Exception as e:
            print(str(e))
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    # @users_ns.doc(description = "Create new user data")
    # @users_ns.expect(users_input_model)
    # @users_ns.marshal_with(users_input_model)
    # def post(self):
    #     """Create new user data"""
    #     try:
    #         data = request.get_json()
    #         bcrypt = current_app.extensions['bcrypt']

    #         input = Users(
    #             email = data.get('email'),
    #             password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8'),
    #             role = data.get('role') if data.get('role') is not None else None
    #         )

    #         print(input)
    #         db.session.add(input)
    #         db.session.commit()

    #         return [], HTTPStatus.CREATED
    #     except Exception as e:
    #         print(e)
    #         users_ns.abort(404, message=str(e))
        
@users_ns.route('/<int:user_id>')
class UserById(Resource):
    @users_ns.doc(description = "Get user data by id", params = {"user_id": "Id user"})
    @users_ns.marshal_list_with(users_output_model)
    @users_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self, user_id):
        """Get user data by id"""
        try:
            data = Users.query.get_or_404(user_id)
            logger.info(f'GET USER WITH ID {data.id}')
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @users_ns.doc(description = "Edit user data by id", params = {"user_id": "Id user"})
    @users_ns.expect(users_input_model)
    @users_ns.marshal_with(users_input_model)
    @users_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def put(self, user_id):
        """Edit user data"""
        email = get_jwt_identity()

        if(checkAuthenticated(user_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO EDIT USER DATA WITH ID {user_id}")
            users_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        data_from_database = Users.query.get_or_404(user_id)
        data = request.get_json(force=True)

        data_from_database.email = data['email']
        data_from_database.role = data['role']
        # data_from_database.password = data['password']
        db.session.commit()

        logger.info(f"PUT USER DATA WITH ID {data_from_database.id}")
        return data_from_database, HTTPStatus.OK
    
    @users_ns.doc(description = "Delete user data by id", params = {"user_id": "Id user"})
    @users_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def delete(self, user_id):
        """Delete user data"""
        email = get_jwt_identity()

        if(checkAuthenticated(user_id, email) is False):
            logger.warning(f"{HTTPStatus.UNAUTHORIZED} - DON'T HAVE PERMISSION TO DELETE USER DATA WITH ID {user_id}")
            users_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        data = Users.query.get_or_404(user_id)

        db.session.delete(data)
        db.session.commit()

        logger.info(f"DELETE USER DATA WITH ID {data.id}")
        return {'message': "Data is succesfully deleted."}, HTTPStatus.OK