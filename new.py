from tensorflow.keras.preprocessing.image import load_img , img_to_array
import tensorflow as tf
import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
import uuid

q_size = 150
classes = ['No_Dr' ,'Mild', 'Moderate' , 'Severe' , 'Proliferative DR']
def predict(filename , model):
    img = cv2.imread(filename)
    img = cv2.resize(img, (q_size, q_size))
    img = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0, 0), 10), -4, 128)
    img_batch = np.expand_dims(img, axis=0)
    pred = model.predict(img_batch)
    pred_classes = np.argmax(pred, axis=1)
    if pred_classes[0]== 0:
        result = 'No_Dr'
    elif pred_classes[0]== 1:
        result = 'Mild'
    elif pred_classes[0]== 2:
        result = 'Moderate'
    elif pred_classes[0]== 3:
        result = 'Severe'
    else:
        result = 'Proliferative DR'

    return result

