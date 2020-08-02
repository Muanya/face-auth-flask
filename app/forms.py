from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	firstName = StringField('FirstName', validators=[DataRequired()])
	lastName = StringField('LastName', validators=[DataRequired()])
	regNo = StringField('RegNo', validators=[DataRequired()])
	password = StringField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')