from app import database as db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager 


class User_Profile(UserMixin, db.Model):
	""" 
		Table class to store the user profile
	"""
	__tablename__ = 'user_profile'

	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String)
	lastName = db.Column(db.String)
	regNo = db.Column(db.String)
	password = db.Column(db.String(128))


	def __init__(self, firstName, lastName, regNo):
		self.firstName = firstName
		self.lastName = lastName 
		self.regNo = regNo

	def __repr__(self):
		return "<regNo {}>".format(self.regNo)



	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password, password)




@login_manager.user_loader
def get_user(id):
	return User_Profile.query.get(int(id))