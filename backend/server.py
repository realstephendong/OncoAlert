from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename #pip install Werkzeug
from flask_cors import CORS #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors

#ML imports
import os
import sys
import glob
import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot
import seaborn as sns
from sklearn import preprocessing, metrics
from sklearn.metrics import confusion_matrix
from keras.applications.vgg16 import VGG16
from keras.models import Model
import xgboost as xgb

#####################################################

app = Flask(__name__)
CORS(app, supports_credentials=True)
 
app.secret_key = "oncoalert-ignition-hacks"
  
UPLOAD_FOLDER = '../assets1/validate/user'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def main():
    return 'Homepage'

@app.route('/analyze')
def analyze():
    # Constants
    IMAGE_SIZE = 256

    # Lists to capture training data and labels
    training_images = []
    training_labels = [] 

    for folder_path in glob.glob("../assets1/train/*"):
        label = folder_path.split("\\")[-1]
        print(label)
        for image_path in glob.glob(os.path.join(folder_path, "*.jpg")):
            print(image_path)
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)       
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            training_images.append(image)
            training_labels.append(label)

    # Convert lists to numpy arrays        
    training_images = np.array(training_images)
    training_labels = np.array(training_labels)

    # Lists to capture test/validation data and labels
    validation_images = []
    validation_labels = [] 
    for folder_path in glob.glob("../assets1/validate/*"):
        label = folder_path.split("\\")[-1]
        print(label)
        for image_path in glob.glob(os.path.join(folder_path, "*.jpg")):
            print(image_path)
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            validation_images.append(image)
            validation_labels.append(label)

    # Convert lists to numpy arrays                
    validation_images = np.array(validation_images)
    validation_labels = np.array(validation_labels)

    # Encode labels from text to integers
    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(validation_labels)
    validation_labels_encoded = label_encoder.transform(validation_labels)
    label_encoder.fit(training_labels)
    training_labels_encoded = label_encoder.transform(training_labels)

    # Split data into train and validation datasets
    x_train, y_train, x_val, y_val = training_images, training_labels_encoded, validation_images, validation_labels_encoded

    # Normalize pixel values to between 0 and 1
    x_train, x_val = x_train / 255.0, x_val / 255.0

    # Load VGG16 model without top layers
    vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

    # Make loaded layers non-trainable
    for layer in vgg16_model.layers:
        layer.trainable = False
        
    vgg16_model.summary()  # Trainable parameters will be 0

    # Use VGG16 features for training
    train_features = vgg16_model.predict(x_train)
    train_features_flattened = train_features.reshape(train_features.shape[0], -1)

    X_train_features = train_features_flattened  # Features for training

    # XGBoost classifier
    import xgboost as xgb
    xgb_model = xgb.XGBClassifier()
    xgb_model.fit(X_train_features, y_train)

    # Process validation data through the same feature extractor
    val_features = vgg16_model.predict(x_val)
    val_features_flattened = val_features.reshape(val_features.shape[0], -1)

    # Predict using the trained model
    predictions = xgb_model.predict(val_features_flattened)
    # Inverse transform to get original labels back
    predictions_labels = label_encoder.inverse_transform(predictions)

    # Check results on a few select images
    index = np.random.randint(0, x_val.shape[0])
    sample_image = x_val[index]
    expanded_image = np.expand_dims(sample_image, axis=0)  # Expand dims for model input
    feature_vector = vgg16_model.predict(expanded_image)
    feature_vector_flattened = feature_vector.reshape(feature_vector.shape[0], -1)
    sample_prediction = xgb_model.predict(feature_vector_flattened)[0] 
    predicted_label = label_encoder.inverse_transform([sample_prediction])  # Get original label
    
    return jsonify({'predicted_label': predicted_label[0]})

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
  
    files = request.files.getlist('files[]')
      
    errors = {}
    success = False
      
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            resp = jsonify({
                "message": 'File type is not allowed',
                "status": 'failed'
            })
            return resp
         
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        errors['status'] = 'failed'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({
            "message": 'Files successfully uploaded',
            "status": 'successs'
        })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run(debug=True)