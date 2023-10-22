from http import HTTPStatus
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from ..utils import db
from ..logs.log import logger
from ..models.users import Users

# namespace digunakan untuk mengelompokkan route yang berkaitan dengan entitas tertentu
# nama namespace digunakan sebagai nama endpoint, nanti jadinya /users
users_ns = Namespace('users', description='Namespace for users')

# .model() digunakan untuk mendefinisikan atribut dari model tersebut
# dapat digunakan untuk melakukan validasi data yang diterima dan memberikan struktur respons
users_model = users_ns.model(
    # mendefinsikan model Users dengan atribut id, username, password
    'Users', {
        'id': fields.Integer(required=True, description="Ini adalah user id"),
        'username': fields.String(description="Ini adalah username"),
        'password': fields.String(description="Ini adalah password"),
    }
)

@users_ns.route('/') # mendefinisikan route /users/
class UserGetPost(Resource):
    # Resource berisi:
    # self - mengakses properti atau metode lain dari kelas Resource
    # args - berisi nilai parameter URL, misal /users/<int:user_id>, jadi bisa mengambil user_id
    # kwargs - berisi nilai parameter query string, misal terdapat parameter ?=name=John, bisa mengambil query name
    # data - berisi json di body request

    # .doc() untuk memberikan keterangan di swagger nya
    @users_ns.marshal_list_with(users_model) # untuk mengonversi banyak objek ke format JSON
    @users_ns.doc(description = "Get all users")
    def get(self):
        """Get all users"""
        try:
            data = Users.query.all()
            logger.info(f"Users data found")
            return data, HTTPStatus.OK
        except Exception as e:
            print(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @users_ns.doc(description = "Create new user data")
    @users_ns.expect(users_model) # menggunakan model 'users_model' untuk validasi input di body
    @users_ns.marshal_with(users_model) # untuk mengonversi satu objek ke format JSON
    def post(self):
        """Create new user data"""
        try:
            # data = users_ns.payload # bisa pakai ini juga
            data = request.get_json()
            print(data)

            input = Users(
                username = data.get('username'),
                password = data.get('password')
            )
            db.session.add(input)
            db.session.commit()

            return [], HTTPStatus.CREATED
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
        
@users_ns.route('/<int:user_id>') # mendefinisikan route /users/{user_id}
class UserById(Resource):
    @users_ns.doc(description = "Get user data by id", params = {"user_id": "Id user"})
    @users_ns.marshal_list_with(users_model)
    def get(self, user_id):
        """Get user data by id"""
        try:
            data = Users.query.get_or_404(user_id)
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @users_ns.doc(description = "Edit user data by id", params = {"user_id": "Id user"})
    @users_ns.expect(users_model)
    @users_ns.marshal_with(users_model)
    def put(self, user_id):
        """Edit user data"""
        try:
            data_from_database = Users.query.get_or_404(user_id)
            data = request.get_json(force=True)

            data_from_database.username = data['username']
            data_from_database.password = data['password']
            db.session.commit()

            return [], HTTPStatus.OK
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @users_ns.doc(description = "Delete user data by id", params = {"user_id": "Id user"})
    @users_ns.marshal_with(users_model)
    def delete(self, user_id):
        """Delete user data"""
        try:
            data = Users.query.get_or_404(user_id)

            db.session.delete(data)
            db.session.commit()

            return [], HTTPStatus.OK
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR