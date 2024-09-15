from flask import Flask, request, jsonify, send_from_directory
import os
import glob
import numpy as np
import cv2
import tensorflow as tf
from sklearn import preprocessing
from keras.applications.vgg16 import VGG16
import xgboost as xgb
from werkzeug.utils import secure_filename
from flask_cors import CORS
import glob

#####################################################
# Constants
IMAGE_SIZE = 64

# Lists to capture training data and labels
training_images = []
training_labels = [] 

for folder_path in glob.glob("../assets1/train/*"):
    label = os.path.basename(folder_path)  # Get folder name as label
    for image_path in glob.glob(os.path.join(folder_path, "*.jpg")):
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
    label = os.path.basename(folder_path)  # Get folder name as label
    for image_path in glob.glob(os.path.join(folder_path, "*.jpg")):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        validation_images.append(image)
        validation_labels.append(label)

# Convert lists to numpy arrays                
validation_images = np.array(validation_images)
validation_labels = np.array(validation_labels)

# Encode labels from text to integers (Fit once on both sets of labels)
label_encoder = preprocessing.LabelEncoder()
all_labels = np.concatenate([training_labels, validation_labels])
label_encoder.fit(all_labels)

# Encode training and validation labels
training_labels_encoded = label_encoder.transform(training_labels)
validation_labels_encoded = label_encoder.transform(validation_labels)

# Split data into train and validation datasets
x_train, y_train, x_val, y_val = training_images, training_labels_encoded, validation_images, validation_labels_encoded

# Normalize pixel values to between 0 and 1
x_train, x_val = x_train / 255.0, x_val / 255.0

# Load VGG16 model without top layers
vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

# Make loaded layers non-trainable
for layer in vgg16_model.layers:
    layer.trainable = False

# Use VGG16 features for training
train_features = vgg16_model.predict(x_train)
train_features_flattened = train_features.reshape(train_features.shape[0], -1)

# XGBoost classifier
xgb_model = xgb.XGBClassifier()
xgb_model.fit(train_features_flattened, y_train)

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
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    if not files:
        return jsonify({'message': 'No images to analyze.', 'status': 'failed'}), 404

    # Select the most recently uploaded image
    latest_file = max(files, key=os.path.getctime)

    # Load and preprocess the image
    image = cv2.imread(latest_file, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = np.expand_dims(image, axis=0)  # Expand dims for model input
    image = image / 255.0  # Normalize pixel values

    # Extract features using VGG16
    feature_vector = vgg16_model.predict(image)
    feature_vector_flattened = feature_vector.reshape(feature_vector.shape[0], -1)

    # Predict using the trained XGBoost model
    prediction = xgb_model.predict(feature_vector_flattened)[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    # Return the prediction result
    return jsonify({'predicted_label': predicted_label})

@app.route('/upload', methods=['POST'])
def upload_file():
    # File upload handling
    if 'files[]' not in request.files:
        resp = jsonify({"message": 'No file part in the request.', "status": 'failed'})
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
            resp = jsonify({"message": 'File type is not allowed.', "status": 'failed'})
            return resp

    if success:
        resp = jsonify({"message": 'File successfully uploaded.', "status": 'success'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

@app.route('/delete', methods=['GET'])
def delete_file():

    success = False
    errors = {}

    try:
        files = glob.glob('../assets1/validate/user/*')
        
        if not files:
            resp = jsonify({"message": "No files to delete.", "status": "failed"}), 404
            return resp
        
        for f in files:
            os.remove(f)
            
        success = True
        if success:
            resp = jsonify({"message": "Files successfully deleted.", "status": "success"})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        
        

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error occurred while deleting files: {str(e)}")
        
        # Return a server error response with the exception details (or a generic message)
        return jsonify({"message": "An error occurred while deleting files.", "error": str(e), "status": "failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
