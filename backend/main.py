import numpy as np 
import matplotlib.pyplot
import glob
import cv2
import tensorflow as tf
from keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization
import seaborn as sns
from keras.applications.vgg16 import VGG16
from sklearn import preprocessing, metrics
from sklearn.metrics import confusion_matrix


import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import sys
sys.stdout.reconfigure(encoding='utf-8')

#OUR DATASET: https://www.kaggle.com/datasets/obulisainaren/multi-cancer
SIZE = 256

t_i = []
t_l = []

for fp in glob.glob("assets/train/*"):
    l = fp.split("\\")[-1]
    print(l)
    for jpgp in glob.glob(os.path.join(fp, "*.jpg")):
        print(jpgp)
        jpg = cv2.imread(jpgp, cv2.IMREAD_COLOR)       
        jpg = cv2.resize(jpg, (SIZE, SIZE))
        jpg = cv2.cvtColor(jpg, cv2.COLOR_RGB2BGR)
        t_i.append(jpg)
        t_l.append(l)

t_i = np.array(t_i)
t_l = np.array(t_l)

tt_i = []
tt_l = []
for fp in glob.glob("assets/validate/*"):
    v_l = fp.split("\\")[-1]
    print(v_l)
    for jpgp in glob.glob(os.path.join(fp, "*.jpg")):
        print(jpgp)
        jpg = cv2.imread(jpgp, cv2.IMREAD_COLOR)
        jpg = cv2.resize(jpg, (SIZE, SIZE))
        jpg = cv2.cvtColor(jpg, cv2.COLOR_RGB2BGR)
        tt_i.append(jpg)
        tt_l.append(v_l)


tt_i = np.array(tt_i)
tt_l = np.array(tt_l)

encoder = preprocessing.LabelEncoder()
encoder.fit(tt_l)
tt_l_encode = encoder.transform(tt_l)
encoder.fit(t_l)
t_l_encode = encoder.transform(t_l)

x_t , y_t, x_tt, y_tt = t_i, t_l_encode, tt_i, tt_l_encode

x_t, x_tt = x_t / 255.0, x_tt / 255.0

VGG = VGG16(weights='imagenet', include_top=False, input_shape=(SIZE, SIZE, 3))

for item in VGG.layers:
	item.trainable = False
    
VGG.summary()

feature_extractor=VGG.predict(x_t)

features = feature_extractor.reshape(feature_extractor.shape[0], -1)
X_for_training = features

#import classifier etc...
import xgboost as xgb
model = xgb.XGBClassifier()
model.fit(X_for_training, y_t)

X_test_feature = VGG.predict(x_tt)
X_test_features = X_test_feature.reshape(X_test_feature.shape[0], -1)

prediction = model.predict(X_test_features) 
prediction = encoder.inverse_transform(prediction)
print ("Accuracy = ", metrics.accuracy_score(tt_l, prediction))
matrix = confusion_matrix(tt_l, prediction)

print(matrix)
sns.heatmap(matrix, annot=True)
matplotlib.pyplot.show()
n=np.random.randint(0, x_tt.shape[0])
png = x_tt[n]
matplotlib.pyplot.imshow(png)
matplotlib.pyplot.show()
i_png = np.expand_dims(png, axis=0)
features = VGG.predict(i_png)
features = features.reshape(features.shape[0], -1)
prediction = model.predict(features)[0] 
prediction = encoder.inverse_transform([prediction])
print("Prediction: ", prediction)
print("Label: ", tt_l[n])