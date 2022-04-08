from flask import url_for, redirect, render_template, flash, abort
from status_page import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from status_page.models import User, Website_data
from status_page.forms import RegistrationForm, LoginForm, registerWebsite, SetWebsiteData

@app.errorhandler(404)
def error_han(e):
	return "404 not found"

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password.')
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # to string
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, has_website='False')
		db.session.add(user)
		db.session.commit()
		flash(f"Your account has been created! You are now able to log in.")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/website', methods=['GET', 'POST'])
def web_pg():
	if current_user.is_authenticated:
		if current_user.has_website == 'False':
			return redirect(url_for('newweb'))
		else:
			web = Website_data.query.filter_by(uid=current_user.id).first()
			return render_template('website.html', ops=web.ops, website_url=web.website_url, named=web.name)

@app.route('/website/new', methods=['GET', 'POST'])
def newweb():
	form = registerWebsite()
	if form.validate_on_submit() and current_user.has_website == 'False':
		web = Website_data(name=form.name.data, website_url=form.website_url.data, truen=str(form.name.data).lower(), author=current_user)
		current_user.has_website = 'True'
		db.session.add(web)
		db.session.commit()
		return redirect(url_for('web_pg'))
	return render_template('new_website.html', form=form)

@app.route('/website/edit', methods=['GET', 'POST'])
def website_edit():
	if current_user.is_authenticated:
		form = SetWebsiteData()
		web_d = Website_data(uid=current_user.id)
		if form.validate_on_submit():
			web_d.name = form.name.data

			web_d.ops = form.ops.data
			web_d.update_latest = form.current_update.data

			web_d.update_past_3 = web_d.update_past_2
			web_d.update_past_3_time = web_d.update_past_2_time

			web_d.update_past_1 = web_d.update_past_1_time
			web_d.update_past_1_time = web_d.update_past_1_time

			web_d.update_past_1 = web_d.update_latest
			web_d.update_past_1_time = web_d.update_latest_time

			web_d.ops = form.ops.data
			web_d.update_latest = form.current_update.data 

			db.session.commit()

			flash('Website updated.')
			return redirect(url_for('website_edit'))

		
		return render_template('website_edit.html', form=form)

@app.route('/<name>')
def get_website(name):
	web = Website_data.query.filter_by(truen=str(name).lower()).first()
	if web == "":
		abort(404)
	else:
		return render_template('status.html', data=web, name=f"{current_user.username}'s Status Page")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route('/', subdomain='<sub_name>')
# def sub_name(sub_name):
# 	site = Website_data.query.filter_by(name=sub_name)
# 	if site == "":
# 		abort(404)
# 	return render_template('status.html', name=f"{sub_name}'s Status Page", data=site)
