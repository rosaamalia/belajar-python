from http import HTTPStatus
from flask import request, jsonify, current_app, Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utils import db
from..utils.utils import checkAuthenticated, checkCourseExist
from ..models.modules import Modules
from ..models.courses import Courses

modules_ns = Namespace('modules', description='Namespace for modules')

modules_input_model = modules_ns.model(
    'ModulesInput', {
        'title': fields.String(),
        'description': fields.String(),
        'content': fields.String(),
        'course_id': fields.Integer()
    }
)

categories_model = modules_ns.model(
    'Categories', {
        'id': fields.Integer(),
        'category_name': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

users_model = modules_ns.model(
    'Users', {
        'id': fields.Integer(),
        'email': fields.String(),
        'role': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

courses_model = modules_ns.model(
    'Courses', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'rating_total': fields.Float(),
        'instructor': fields.Nested(users_model),
        'category': fields.Nested(categories_model),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

modules_output_model = modules_ns.model(
    'ModulesOutput', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'content': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
        'course': fields.Nested(courses_model)
    }
)

@modules_ns.route('/')
class ModuleGetPost(Resource):
    @modules_ns.marshal_list_with(modules_output_model)
    @modules_ns.doc(description = "Get all modules")
    @modules_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self):
        """Get all modules"""
        try:
            data = Modules.query.all()
            return data, HTTPStatus.OK
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @modules_ns.doc(description = "Create new module data")
    @modules_ns.expect(modules_input_model)
    @modules_ns.marshal_with(modules_input_model)
    @modules_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def post(self):
        """Create new module data"""
        # data = modules_ns.payload # bisa pakai ini juga
        data = modules_ns.payload
        
        # cek course tersedia
        if(checkCourseExist(data.get('course_id')) is False):
            modules_ns.abort(HTTPStatus.BAD_REQUEST, message="Course is not found.")
        
        course = Courses.query.get(data.get('course_id'))

        email = get_jwt_identity()
        if(checkAuthenticated(course.instructor_id, email) is False):
            modules_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        module = Modules(**data)

        print(module)
        db.session.add(module)
        db.session.commit()

        return module, HTTPStatus.CREATED
        
@modules_ns.route('/<int:module_id>')
class ModuleById(Resource):
    @modules_ns.doc(description = "Get module data by id", params = {"module_id": "Id module"})
    @modules_ns.marshal_list_with(modules_output_model)
    @modules_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self, module_id):
        """Get module data by id"""
        try:
            data = Modules.query.get_or_404(module_id)
            return data, HTTPStatus.OK

        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @modules_ns.doc(description = "Edit module data by id", params = {"module_id": "Id module"})
    @modules_ns.expect(modules_input_model)
    @modules_ns.marshal_with(modules_input_model)
    @modules_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def put(self, module_id):
        """Edit module data"""
        data_from_database = Modules.query.get_or_404(module_id)
        data = request.get_json(force=True)

        course = Courses.query.get(data_from_database.course_id)

        email = get_jwt_identity()
        if(checkAuthenticated(course.instructor_id, email) is False):
            modules_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        data_from_database.title = data['title']
        data_from_database.description = data['description']
        data_from_database.content = data['content']
        data_from_database.course_id = data['course_id']

        db.session.commit()

        return data_from_database, HTTPStatus.OK
    
    @modules_ns.doc(description = "Delete module data by id", params = {"module_id": "Id module"})
    @modules_ns.marshal_with(modules_input_model)
    @modules_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def delete(self, module_id):
        """Delete module data"""
        data = Modules.query.get_or_404(module_id)

        course = Courses.query.get(data.course_id)

        email = get_jwt_identity()
        if(checkAuthenticated(course.instructor_id, email) is False):
            modules_ns.abort(HTTPStatus.UNAUTHORIZED, message="You don't have permission to do this action.")

        db.session.delete(data)
        db.session.commit()

        return {'message': "Data is succesfully deleted."}, HTTPStatus.OK