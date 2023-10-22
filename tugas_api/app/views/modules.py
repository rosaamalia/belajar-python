from http import HTTPStatus
from flask import request, jsonify, current_app, Response
from flask_restx import Namespace, Resource, fields

from ..utils import db
from..utils.utils import checkCourseExist
from ..models.modules import Modules

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
    def post(self):
        """Create new module data"""
        # data = modules_ns.payload # bisa pakai ini juga
        data = modules_ns.payload
        
        # cek course tersedia
        if(checkCourseExist(data.get('course_id')) is False):
            modules_ns.abort(HTTPStatus.BAD_REQUEST, message="Course is not found.")

        module = Modules(**data)

        print(module)
        db.session.add(module)
        db.session.commit()

        return module, HTTPStatus.CREATED
        
@modules_ns.route('/<int:module_id>')
class ModuleById(Resource):
    @modules_ns.doc(description = "Get module data by id", params = {"module_id": "Id module"})
    @modules_ns.marshal_list_with(modules_output_model)
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
    def put(self, module_id):
        """Edit module data"""
        try:
            data_from_database = Modules.query.get_or_404(module_id)
            data = request.get_json(force=True)

            data_from_database.title = data['title']
            data_from_database.description = data['description']
            data_from_database.content = data['content']
            data_from_database.course_id = data['course_id']

            db.session.commit()

            return [], HTTPStatus.OK
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @modules_ns.doc(description = "Delete module data by id", params = {"module_id": "Id module"})
    @modules_ns.marshal_with(modules_input_model)
    def delete(self, module_id):
        """Delete module data"""
        try:
            data = Modules.query.get_or_404(module_id)

            db.session.delete(data)
            db.session.commit()

            return [], HTTPStatus.OK
        except Exception as e:
            return [], HTTPStatus.INTERNAL_SERVER_ERROR