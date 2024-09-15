import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2
import tensorflow as tf
from keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.applications.vgg16 import VGG16
from sklearn import preprocessing, metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns
import xgboost as xgb
import os
import sys

# Ensure TensorFlow uses only CPU if you don't have GPU support
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Ensure UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Constants
SIZE = 128

# Function to process images
def process_images(directory):
    images, labels = [], []
    for fp in glob.glob(f"{directory}/*"):
        label = os.path.basename(fp)
        for jpgp in glob.glob(os.path.join(fp, "*.jpg")):
            img = cv2.imread(jpgp, cv2.IMREAD_COLOR)
            if img is not None:
                img = cv2.resize(img, (SIZE, SIZE))
                images.append(img)
                labels.append(label)
    return np.array(images), np.array(labels)

# Load and process dataset
train_images, train_labels = process_images("assets/train")
val_images, val_labels = process_images("assets/validate")

# Label encoding
encoder = preprocessing.LabelEncoder()
encoder.fit(train_labels)
train_labels_encoded = encoder.transform(train_labels)
val_labels_encoded = encoder.transform(val_labels)

# Normalize images
train_images, val_images = train_images / 255.0, val_images / 255.0

# Load VGG16 model
vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(SIZE, SIZE, 3))
for layer in vgg_model.layers:
    layer.trainable = False
vgg_model.summary()

# Extract features
train_features = vgg_model.predict(train_images)
train_features = train_features.reshape(train_features.shape[0], -1)

# Train XGBoost model
xgb_model = xgb.XGBClassifier()
xgb_model.fit(train_features, train_labels_encoded)

# Predict and evaluate
val_features = vgg_model.predict(val_images)
val_features = val_features.reshape(val_features.shape[0], -1)
predictions = xgb_model.predict(val_features)
predictions = encoder.inverse_transform(predictions)

print("Accuracy = ", metrics.accuracy_score(val_labels, predictions))
conf_matrix = confusion_matrix(val_labels, predictions)

sns.heatmap(conf_matrix, annot=True)
plt.show()

# Show random image and prediction
n = np.random.randint(0, val_images.shape[0])
random_img = val_images[n]
plt.imshow(random_img)
plt.show()

img_features = np.expand_dims(random_img, axis=0)
img_features = vgg_model.predict(img_features)
img_features = img_features.reshape(img_features.shape[0], -1)
img_prediction = xgb_model.predict(img_features)[0]
img_prediction = encoder.inverse_transform([img_prediction])

print("Prediction: ", img_prediction)
print("Label: ", val_labels[n])