from flask import render_template, request, redirect
from flask import url_for, flash
from flask_login import current_user, login_user
from flask_login import logout_user
from app import app
from app.forms import LoginForm 
from app.models import User_Profile as user
import app.processing as pr 
import os



@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('pictureCapture.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		usr = user.query.filter_by(regNo=form.regNo.data).first()
		if usr is None or not usr.check_password(form.password.data):
			flash('Incorrect registration number or password')
			return redirect('/login')
		# login_user(usr, remember=form.remember_me.data)
		return redirect(url_for('picture_verify', usr=usr.id))
	return render_template('sign_in.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/pic', methods=['POST', 'GET'])
def picture_verify():
	get_id = int(request.args.get('usr'))
	usr = user.query.get(get_id)
	print(usr)

	if request.method == 'POST':
		form = request.form
		image_b64 = form['b64_image']
		decoded_img = pr.decode_base64(image_b64)
		face_encoding = pr.facial_encode(decoded_img)

		if face_encoding.all() == 0:
			flash('Could not find a face in the picture. Try Adjusting the lighting conditions')
			return redirect(url_for('picture_verify', usr=usr.id))

		# file_url = os.path.join(app.config['UPLOAD_FOLDER'], '2016_232383')
		# pr.save_enc(file_url, face_encoding)
		test_url = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
		test_data = pr.load_enc(test_url)
		match = pr.match_encodings(test_data, face_encoding)
		dist = pr.face_distance(test_data, face_encoding)
		print(dist)
		if match:
			print('Nwokeji Peter Chimuanya')
			login_user(usr)
			flash('Succesfully Logged in')
			return redirect(url_for('login'))
		else:
			print('Face does not match the test data')
			flash('Failed to log in. Face does not match')
			return redirect(url_for('login'))
		#print(data)


		#print(face_encoding)
	return render_template('pictureCapture.html', user_id=usr.id)
