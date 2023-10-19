from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from .config.config import config_dict
from .views.users import users_ns
from .utils import db
from .models import users

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    api = Api(
        app,
        doc="/docs",
        title="REST API FLASK",
        description="Latihan membuat API"
    )

    api.add_namespace(users_ns)

    migrate = Migrate(app, db)

    return app