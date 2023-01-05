from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from time import sleep
import requests
import os
region = "eastus"
key = "c765f90338c64b209ba5842838aeb67d"
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(
    endpoint="https://julian.cognitiveservices.azure.com/",
    credentials=credentials
) 
def transcript_file(file):
    url = "https://lab3up.azurewebsites.net/api/Picture?id=1"
    name = 'static/uploads/' + file 
    text=''
    data = open(name,'rb').read()
    requests.post(url, data=data)

    # # url = "https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/raw/master/samples/vision/images/make_things_happen.jpg"
    # raw = True
    # numberOfCharsInOperationId = 36

    # # SDK call
    # rawHttpResponse = client.read(url, language="en", raw=True)

    # # Get ID from returned headers
    # operationLocation = rawHttpResponse.headers["Operation-Location"]
    # idLocation = len(operationLocation) - numberOfCharsInOperationId
    # operationId = operationLocation[idLocation:]

    # # SDK call
    # result = client.get_read_result(operationId)

    # while result.status != OperationStatusCodes.succeeded:
    #     # print(result.status)
    #     sleep(1)
    #     result = client.get_read_result(operationId)
    # # Get data
    # if result.status == OperationStatusCodes.succeeded:
    #     for line in result.analyze_result.read_results[0].lines:
    #         text = text  + line.text + '\n'
    return text

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        transcription = transcript_file(filename)
       
        return render_template('index.html', transcription=transcription , filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
if __name__ == "__main__":
    app.run()