from flask import Flask

from app.config import get_config
from app.extensions import db, cache
from app.api.v1.routes import api_bp
from app.frontend.routes.routes import UIController


def create_app(config_name="dev"):
    """
    Create and configure the Flask application.

    :param config_name: Configuration name, defaults to 'dev'.
    """
    app = Flask(__name__)
    ui_controller = UIController()

    app.config.from_object(get_config(config_name))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'

    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(ui_controller.bp)

    app.app_context()

    with app.app_context():
        db.create_all()

    return app
