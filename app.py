import os
import uuid
import flask
import urllib
# from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file, session
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from new import predict
from werkzeug.utils import secure_filename




UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# PEOPLE_FOLDER = os.path.join('staticFiles', 'staticfile')
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'final.h5'))
 
@app.route('/')
def index():
    no_dr = os.path.join(UPLOAD_FOLDER, 'staticfile/No_dr.png')
    Mild = os.path.join(UPLOAD_FOLDER, 'staticfile/Mild.png')
    Moderate = os.path.join(UPLOAD_FOLDER, 'staticfile/Moderate.png')
    Severe = os.path.join(UPLOAD_FOLDER, 'staticfile/Severe.png')
    Proliferative_DR = os.path.join(UPLOAD_FOLDER, 'staticfile/Proliferative_DR.png')
    return render_template('index_upload_and_show_data.html',no_dr = no_dr,Mild=Mild,Moderate=Moderate,Severe=Severe,Proliferative_DR=Proliferative_DR)
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
   
    if request.method == 'POST':
        no_dr = os.path.join(UPLOAD_FOLDER, 'staticfile/No_dr.png')
        Mild = os.path.join(UPLOAD_FOLDER, 'staticfile/Mild.png')
        Moderate = os.path.join(UPLOAD_FOLDER, 'staticfile/Moderate.png')
        Severe = os.path.join(UPLOAD_FOLDER, 'staticfile/Severe.png')
        Proliferative_DR = os.path.join(UPLOAD_FOLDER, 'staticfile/Proliferative_DR.png')
        # Upload file flask
        try:
            uploaded_img = request.files['uploaded-file']
            # Extracting uploaded data file name
            img_filename = secure_filename(uploaded_img.filename)
            # Upload file to database (defined uploaded folder in static path)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            # Storing uploaded file path in flask session
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        except:
            print('Please select an image')
        return render_template('index_upload_and_show_data_page2.html',no_dr = no_dr,Mild=Mild,Moderate=Moderate,Severe=Severe,Proliferative_DR=Proliferative_DR)
 
@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    
    img_file_path = session.get('uploaded_img_file_path', None)
   #  print('***')
    print(img_file_path)
    img_path = os.path.join(BASE_DIR , img_file_path)

    result = predict(img_path,model)

    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path, result= result)

if __name__ == '__main__':
   app.run(debug = True)