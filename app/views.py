from flask import render_template, request, redirect
from flask import url_for, flash
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app import app, database
from app.forms import LoginForm, SignUpForm 
from app.models import User_Profile as user
import app.processing as pr 
import os
import requests


@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('logged_in'))

	form = SignUpForm()


	if form.validate_on_submit():
		usr = user(firstName=form.firstName.data, lastName=form.lastName.data, regNo=form.regNo.data)
		usr.set_password(form.password.data)
		database.session.add(usr)
		database.session.commit()
		return  redirect(url_for('picture_upload', usr=pr.encoding_int(usr.id), token=pr.token_key))


	return render_template('register.html', form=form)




@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('logged_in'))

	form = LoginForm()

	if form.validate_on_submit():
		usr = user.query.filter_by(regNo=form.regNo.data).first()
		if usr is None or not usr.check_password(form.password.data):
			flash('Incorrect registration number or password')
			return redirect('/login')
		# login_user(usr, remember=form.remember_me.data)
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('picture_verify', usr=pr.encoding_int(usr.id), token=pr.token_key))

		return redirect(url_for('picture_verify', usr=pr.encoding_int(usr.id), token=pr.token_key, next=next_page))
	return render_template('sign_in.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))




@app.route('/pic_upload', methods=['POST', 'GET'])
def picture_upload():
	try:
		user_id = pr.decoding_int(request.args.get('usr'))
	except:
		flash('method not acceptable!')
		return redirect(url_for('register'))

	if pr.token_key != request.args.get('token'):
		return redirect(url_for('index'))

	usr = user.query.get(user_id)

	if request.method == 'POST':
		image_b64 = request.form['b64_image']
		decoded_img = pr.decode_base64(image_b64)
		face_encoding = pr.facial_encode(decoded_img)

		if face_encoding.all() == 0:
			flash('Could not find a face in the picture. Try Adjusting the lighting conditions')
			return redirect(url_for('picture_upload', usr=pr.encoding_int(usr.id), token=pr.token_key))

		file_url = os.path.join(app.config['UPLOAD_FOLDER'], usr.regNo.replace('/', '_'))
		pr.save_enc(file_url, face_encoding)
		usr.set_uploaded_image()
		database.session.commit()
		flash("You have Succesfully registered!")
		return redirect(url_for('login'))
	
	return render_template('picture_upload.html', usr_enc=pr.encoding_int(usr.id), token_key=pr.token_key)





@app.route('/pic', methods=['POST', 'GET'])
def picture_verify():
	try:
		user_id = pr.decoding_int(request.args.get('usr'))
	except:
		flash('method not acceptable!')
		return redirect(url_for('login'))
		
	

	if pr.token_key != request.args.get('token'):
		flash('method not acceptable! Sign In first!')
		return redirect(url_for('login'))

	usr = user.query.get(user_id)
	print(usr)

	if not usr.has_uploaded_image():
		flash('You have not completed registration. Please upload image to complete it!')
		return redirect(url_for('picture_upload', usr=pr.encoding_int(usr.id), token=pr.token_key))

	if request.method == 'POST':
		form = request.form
		image_b64 = form['b64_image']
		decoded_img = pr.decode_base64(image_b64)
		face_encoding = pr.facial_encode(decoded_img)

		if face_encoding.all() == 0:
			flash('Could not find a face in the picture. Try Adjusting the lighting conditions')
			return redirect(url_for('picture_verify', usr=pr.encoding_int(usr.id), token=pr.token_key))

		test_url = os.path.join(app.config['UPLOAD_FOLDER'], usr.regNo.replace('/', '_'))
		test_data = pr.load_enc(test_url)
		match = pr.match_encodings(test_data, face_encoding)
		dist = pr.face_distance(test_data, face_encoding)
		print(dist)
		if match:
			print('Nwokeji Peter Chimuanya')
			login_user(usr)
			flash('Succesfully Logged in')
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page) != '':
				return redirect(url_for('logged_index'))
			return redirect(next_page)
		else:
			print('Face does not match the test data')
			flash('Failed to log in. Face does not match')
			return redirect(url_for('login'))


	return render_template('pictureCapture.html', usr_enc=pr.encoding_int(usr.id), token_key=pr.token_key)

@app.route('/welcome')
@login_required
def logged_index():
	return render_template('success.html')



