import os 

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	"""
		Parent Config Class
	"""
	DEBUG = False
	CSRF_ENABLED = True
	SECRET_KEY = '4zQnhnJ--zjWoOqsEFLXMImma5tnmshNXN5E-dobXSc'
	TESTING = False
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] # 'sqlite:///'+os.path.join(base_dir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOAD_FOLDER = os.path.join(base_dir, 'face_enc')

class DevelopmentConfig(Config):
	"""
		Config Class for development
	"""
	DEBUG = True
	DEVELOPMENT = True
	
