from status_page import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id): # load user to login
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	# uuid = db.Column(db.String, unique=True, nullable=False)
	username = db.Column(db.String(18), unique=True, nullable=False)
	email = db.Column(db.String(60), unique=True, nullable=False)
	# image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
	password = db.Column(db.String(30), nullable=False)
	has_website = db.Column(db.String(6), nullable=True)
	wb_data = db.relationship('Website_data', backref='author', lazy=True)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.password}')"

class Website_data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(16), unique=True)
	truen = db.Column(db.String(16), unique=False)
	website_url = db.Column(db.String(30), unique=False, nullable=False)
	ops = db.Column(db.String(51), unique=False, nullable=True)
	update_latest = db.Column(db.String(200), unique=False, nullable=True)
	update_latest_time = db.Column(db.DateTime, nullable=True)
	update_past_1 = db.Column(db.String(200), unique=True)
	update_past_1_time = db.Column(db.DateTime, nullable=True)
	update_past_2 = db.Column(db.String(200), unique=True)
	update_past_2_time = db.Column(db.DateTime, nullable=True)
	update_past_3 = db.Column(db.String(200), unique=True)
	update_past_3_time = db.Column(db.DateTime, nullable=True)
	# past_5 = db.Column(db.String, unique=False)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

	def __repr__(self):
		return f"Website_data('{self.name}', '{self.truen}', '{self.website_url}', '{self.ops}')"