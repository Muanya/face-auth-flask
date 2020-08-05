from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User_Profile


class LoginForm(FlaskForm):
	regNo = StringField('Registration No.', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
	firstName = StringField('FirstName', validators=[DataRequired()])
	lastName = StringField('LastName', validators=[DataRequired()])
	regNo = StringField('Registration No.', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_regNo(self, reg_no):
		regno = User_Profile.query.filter_by(regNo=reg_no.data).first()

		if regno is not None:
			raise ValidationError('Registration number already exist')

