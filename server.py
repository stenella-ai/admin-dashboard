import os

from flask import Flask
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

import waitress
from werkzeug.middleware.proxy_fix import ProxyFix


def init():
    if os.path.exists('.env'):
        load_dotenv('.env')
    else:
        raise Exception('could not find a .env file')
    return Flask(__name__)

def configure(app):
    app.secret_key = b'e0f34b5a8213b678cdd256f8ba071e6132008bc993e578b5f907207dc0289d65'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'mysql+pymysql://{os.environ.get("dbuser")}:{os.environ.get("dbpass")}@test-mysql-database.c5uc0isoumxu.us-east-2.rds.amazonaws.com/countpool?charset=utf8mb4'
    return app

def generate_flask_extensions(app):
    login_database = SQLAlchemy(app)
    migrate = Migrate(app, login_database)
    login = LoginManager(app)
    login.login_view = 'login'
    return app, login_database, login

def generate_routes(): import routes;


app, login_database, login = generate_flask_extensions(configure(init()))
with app.app_context():
    current_app.login_database = login_database
    current_app.login = login
    generate_routes()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
waitress.serve(app, host='127.0.0.1', port=8000, url_scheme='https')