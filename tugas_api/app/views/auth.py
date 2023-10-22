from http import HTTPStatus
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from ..utils import db
from ..utils.utils import checkUserEmailExist
from ..logs.log import logger
from ..models.users import Users

auth_ns = Namespace('auth', description='Namespace for authentication')

register_model = auth_ns.model(
    'RegisterInput', {
        'email': fields.String(),
        'password': fields.String(),
        'role': fields.String(),
    }
)

register_output_model = auth_ns.model(
    'RegisterOutput', {
        'email': fields.String(),
        'access_token': fields.String(),
        'refresh_token': fields.String()
    }
)

login_input_model = auth_ns.model(
    'LoginInput', {
        'email': fields.String(),
        'password': fields.String()
    }
)

refreh_input_model = auth_ns.model(
    'RefreshInput', {
        'refresh_token': fields.String()
    }
)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.doc(description = "Create new user data")
    @auth_ns.expect(register_model)
    @auth_ns.marshal_with(register_output_model)
    def post(self):
        """Create new user data"""
        data = request.get_json()
        bcrypt = current_app.extensions['bcrypt']

        # Cek email sudah ada atau belum
        if(checkUserEmailExist(data.get('email')) is True):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH EMAIL {data.get('email')} IS ALREADY EXIST")
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Email is already taken.")

        input = Users(
            email = data.get('email'),
            password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8'),
            role = data.get('role') if data.get('role') is not None else None
        )

        db.session.add(input)
        db.session.commit()

        access_token = create_access_token(identity=input.email)
        refresh_token = create_refresh_token(identity=input.email)

        logger.info(f"CREATE USER WITH EMAIL {data.get('email')}")

        return {'email': input.email, 'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED

@auth_ns.route('/signin')
class SignUp(Resource):
    @auth_ns.doc(description = "Login to system")
    @auth_ns.expect(login_input_model)
    def post(self):
        """Login to system"""
        data = request.get_json()
        bcrypt = current_app.extensions['bcrypt']

        user = Users.query.filter_by(email=data.get('email')).first()
        
        if(not user):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - USER WITH EMAIL {data.get('email')} IS NOT FOUND")
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Email is not found.")

        checkPassword = bcrypt.check_password_hash(user.password, data.get('password'))

        if(checkPassword is False):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - PASSWORD OF USER WITH EMAIL {data.get('email')} IS INCORRECT")
            auth_ns.abort(HTTPStatus.BAD_REQUEST, message="Password is incorrect.")

        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        logger.info(f"USER DATA WITH ID {user.id} IS LOGGED IN")
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED

@auth_ns.route('/refresh')
class Refresh(Resource):
    @auth_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Refresh Token'}})
    @auth_ns.expect(refreh_input_model)
    @jwt_required(refresh=True)
    def post(self):
        """Get refreshed token"""
        data = request.get_json()
        email = get_jwt_identity()

        access_token = create_access_token(identity=email, fresh=True)
        logger.info(f"USER DATA WITH EMAIL {email} GET REFRESHED TOKEN")
        return {'access_token': access_token, 'refresh_token': data.get('refresh_token')}, HTTPStatus.CREATED
    