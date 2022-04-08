from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from status_page.models import User, Website_data
from datetime import datetime

class RegistrationForm(FlaskForm):
	username = StringField('Username',
	 						validators=[DataRequired(),
	 						Length(min=2, max=16)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
									validators=[DataRequired(), 
									EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken.')

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me?')
	submit = SubmitField('Login')

class registerWebsite(FlaskForm):
	name = StringField('Enter website name', validators=[DataRequired(),
	 						Length(min=1, max=16)])

	website_url = StringField('Enter website url', validators=[DataRequired(),
	 						Length(min=1, max=50)])

	submit = SubmitField('Create website!')

	def validate_name(self, name):
		website_name = Website_data.query.filter_by(name=str(name)).first()
		if website_name:
			raise ValidationError('That website name is taken.')

class SetWebsiteData(FlaskForm):
	name = StringField('Name', validators=[DataRequired(),
	 						Length(min=2, max=16)])
	website_url = StringField('Update URL', validators=[DataRequired(),
	 						Length(min=2, max=30)])
	# ops = SelectField('Operation', 
	# 	choices=[('0', 'All Normal'), ('1', 'Minor Issues'), ('2', 'Major Issues'), ('3', 'System Outage')])

	ops = StringField('Current Operation', validators=[DataRequired(),
	 						Length(min=2, max=50)])

	current_update = StringField('Enter current update.', validators=[DataRequired(),
	 						Length(min=2, max=200)])
	submit = SubmitField('Publish Update')
