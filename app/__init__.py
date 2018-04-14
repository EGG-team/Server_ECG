# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

app = Flask(__name__)
app.config.update(
    dict(
        SECRET_KEY="powerful-secretkey",
        WTF_CSRF_SECRET_KEY="a-csrf-secret-key",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format('root', 'myivan', 'localhost', '3306', 'ecg_db')
    )
)
# sslify = SSLify(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import routes
from app import api
from app import models
from app import forms