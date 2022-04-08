from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd746af6536733582e968588a522b5b7efc4c7f4b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# Go to outside of lowest status folder than import and do db.create_all()
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from status_page import routes