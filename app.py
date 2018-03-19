from flask import Flask, render_template, request 
from flask_uploads import UploadSet, configure_uploads, IMAGES
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = './data'
configure_uploads(app, photos)

# Instantiates a client
client = vision.ImageAnnotatorClient()
result = ''

@app.route('/', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		image_location = ('./data/'+filename)
        #encoded_image = encode(image)

		# Loads the image into memory
		with io.open(image_location, 'rb') as image_file:
			content = image_file.read()
		
		image = types.Image(content=content)

		# Performs label detection on the image file
		response = client.web_detection(image=image)
		labels = response.web_detection.web_entities
		
		#check to see if elon musk is first in the labels:
		for entity in labels:
			print(entity.description)
			if entity.description == 'Elon Musk':
				result = 'Elon Musk'
				print(entity.score)
				break
			else: 
				result = 'not Elon Musk'

		return render_template('result.html', result = result)
	return render_template('index.html')

@app.route('/result')
def result():
	return render_template('result.html', result = result)
# def encode(image_address):
# 	with open(image_address, "rb") as image_file:
#    		encoded_string = base64.b64encode(image_file.read())
#    		return encoded_string

if __name__ == '__main__':
    app.run(port=80, debug=True)