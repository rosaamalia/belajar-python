from http import HTTPStatus
from flask import request, jsonify, current_app, Response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required

from ..utils import db
from ..utils.utils import checkCategoryNameExist
from ..logs.log import logger
from ..models.categories import Categories

categories_ns = Namespace('categories', description='Namespace for categories')

categories_input_model = categories_ns.model(
    'CategoriesInput', {
        'category_name': fields.String(),
    }
)

users_model = categories_ns.model(
    'Users', {
        'id': fields.Integer(),
        'email': fields.String(),
        'role': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

courses_model = categories_ns.model(
    'Courses', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
        'rating_total': fields.Float(),
        'category_id': fields.Integer(),
        'instructor': fields.Nested(users_model),
        'created_at': fields.String(),
        'updated_at': fields.String(),
    }
)

categories_get_model = categories_ns.model(
    'Categories', {
        'id': fields.Integer(),
        'category_name': fields.String(),
        'created_at': fields.String(),
        'updated_at': fields.String(),
        'courses': fields.List(fields.Nested(courses_model))
    }
)

@categories_ns.route('/')
class CategoryGetPost(Resource):
    @categories_ns.marshal_list_with(categories_get_model)
    @categories_ns.doc(description = "Get all categories")
    @categories_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self):
        """Get all categories"""
        try:
            data = Categories.query.all()
            logger.info(f"GET ALL CATEGORY DATA")
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @categories_ns.doc(description = "Create new category data")
    @categories_ns.expect(categories_input_model)
    @categories_ns.marshal_with(categories_input_model)
    @categories_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def post(self):
        """Create new category data"""
        # data = categories_ns.payload # bisa pakai ini juga
        data = request.get_json()
        print(data)

        # Cek nama kategori sudah ada
        if(checkCategoryNameExist(data.get('category_name')) is True):
            logger.warning(f"{HTTPStatus.BAD_REQUEST} - CATEGORY NAME {data.get('category_name')} IS ALREADY EXIST")
            categories_ns.abort(HTTPStatus.BAD_REQUEST, message="Name of the category is already exist.")

        input = Categories(
            category_name = data.get('category_name'),
        )

        db.session.add(input)
        db.session.commit()

        logger.info(f"POST CATEGORY DATA WITH ID {input.id}")
        return input, HTTPStatus.CREATED
        
@categories_ns.route('/<int:category_id>')
class CategoryById(Resource):
    @categories_ns.doc(description = "Get category data by id", params = {"category_id": "Id category"})
    @categories_ns.marshal_list_with(categories_get_model)
    @categories_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def get(self, category_id):
        """Get category data by id"""
        try:
            data = Categories.query.get_or_404(category_id)
            logger.info(f"GET CATEGORY DATA WITH ID {data.id}")
            return data, HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @categories_ns.doc(description = "Edit category data by id", params = {"category_id": "Id category"})
    @categories_ns.expect(categories_input_model)
    @categories_ns.marshal_with(categories_input_model)
    @categories_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def put(self, category_id):
        """Edit category data"""
        try:
            data_from_database = Categories.query.get_or_404(category_id)
            data = request.get_json(force=True)

            data_from_database.category_name = data['category_name']

            db.session.commit()
            logger.info(f"PUT CATEGORY DATA WITH ID {data_from_database.id}")
            return [], HTTPStatus.OK
        except Exception as e:
            logger.error(str(e))
            return [], HTTPStatus.INTERNAL_SERVER_ERROR
    
    @categories_ns.doc(description = "Delete category data by id", params = {"category_id": "Id category"})
    @categories_ns.marshal_with(categories_input_model)
    @categories_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Access Token'}})
    @jwt_required()
    def delete(self, category_id):
        """Delete category data"""
        data = Categories.query.get_or_404(category_id)

        db.session.delete(data)
        db.session.commit()

        logger.info(f"DELETE CATEGORY DATA WITH ID {data.id}")
        return {'message': "Data is succesfully deleted."}, HTTPStatus.OK