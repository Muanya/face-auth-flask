import cv2
import face_recognition
import numpy as np 
import base64

def decode_base64(url):
	encoded_image = url.split(',')[1]
	decoded_image = base64.b64decode(encoded_image)
	nparr = np.fromstring(decoded_image, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img 

def facial_encode(img):
	# generate the face encodings
	face_encode = face_recognition.face_encodings(img)

	if(len(face_encode) == 1):
		# generate facial encodings
		return face_encode[0]
	elif(len(face_encode) > 1):
		print("Image contains more than one face...")
		print("Using the first face detected.../")
		return face_encode[0]
	else:
		print("No face found")
		return np.array([0])

def match_encodings(encoding1, encoding2):
	result = face_recognition.compare_faces([encoding1], encoding2, tolerance=0.5)
	return result[0]

def face_distance(encoding1, encoding2):
	face_distances = face_recognition.face_distance([encoding1], encoding2)
	return face_distances


def save_enc(url, encodings):
	# add extension of the file 
	url+= '.npy'

	# save the file in npy format 
	np.save(url, encodings)

def load_enc(url):
	# add extension
	url +='.npy'

	# load the data
	data = np.load(url)
	return data
