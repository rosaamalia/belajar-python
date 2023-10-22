from flask import Flask, current_app
from flask_restx import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from .config.config import config_dict
from .views.users import users_ns
from .views.courses import courses_ns
from .views.categories import categories_ns
from .views.enrollments import enrollments_ns
from .views.modules import modules_ns
from .utils import db
from .models import users, courses, categories, modules, enrollments

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    api = Api(
        app,
        doc="/docs",
        title="REST API COURSE ONLINE",
        description="COURSE ONLINE"
    )

    api.add_namespace(users_ns)
    api.add_namespace(courses_ns)
    api.add_namespace(categories_ns)
    api.add_namespace(enrollments_ns)
    api.add_namespace(modules_ns)

    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    
    with app.app_context():
        current_app.extensions['bcrypt'] = bcrypt

    return app