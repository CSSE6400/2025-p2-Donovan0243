from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app == Flask framework
def create_app(config_overrides=None):
    app = Flask(__name__)  # Initialize the Flask application


# 1. db configuration 
    # Configure the SQLite database URI (file-based storage)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
    if config_overrides:
        app.config.update(config_overrides)

    # Load the models and initialize the database
    from todo.models import db
    from todo.models.todo import Todo
    db.init_app(app)

    # Create the database tables if they do not exist
    with app.app_context():
        db.create_all()
        db.session.commit()


# 2. APIs configuration 
    # Register the API blueprints (routes)
    from todo.views.routes import api
    app.register_blueprint(api)

    return app  # Return the configured Flask app
