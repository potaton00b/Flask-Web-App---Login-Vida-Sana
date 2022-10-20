from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
DB_MYSQLNAME = "users"
usingMySql = True

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # Google Cloud SQL (change this accordingly)
    PASSWORD ="fitbitdata!"
    PUBLIC_IP_ADDRESS ="34.125.228.17"
    DBNAME ="testing"
    PROJECT_ID ="som-vidasana"
    INSTANCE_NAME ="fitbitdata"


    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:Ha5xng56@localhost/{DB_MYSQLNAME}' <- local mysql

    # configuration
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://root:fitbitdata!@34.125.228.17/testing?unix_socket=/cloudsql/som-vidasana:fitbitdata'
    #app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://root:fitbitdata!@34.125.228.17/testing?unix_socket=/cloudsql/som-vidasana:fitbitdata'
    #app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = ""
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME) or usingMySql == True:
        db.create_all(app=app)
        print('Created Database!')
