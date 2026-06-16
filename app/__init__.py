from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'cci-surveyhub-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveyhub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.surveys import surveys
    from app.routes.responses import responses
    from app.routes.exports import exports

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(surveys)
    app.register_blueprint(responses)
    app.register_blueprint(exports)

    with app.app_context():
        from app.models.user import User
        from app.models.survey import Survey, Block, Question, Choice
        from app.models.response import Company, Response, Answer
        from app.models.anomaly import Anomaly
        db.create_all()

    return app