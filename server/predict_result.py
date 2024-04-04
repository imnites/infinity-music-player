import cv2
import numpy as np
import tensorflow as tf
import base64
from PIL import Image
import io
import codecs
import os
import dlib


emotion_labels = sorted(os.listdir('./input/CK+48'))

model = tf.keras.models.load_model('./output/emotion_model_pretrained.keras')

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

detector = dlib.get_frontal_face_detector()

def get_emotion_predictions(face_img):
    face_img = cv2.imread(face_img, cv2.COLOR_BGR2GRAY)
    try:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    except:
        pass
    
    rects = detector(face_img , 0)
    if len(rects) >= 1 :
        for rect in rects :
            (x , y , w , h) = rect_to_bb(rect)
            img = face_img[y-10 : y+h+10 , x-10 : x+w+10]

            if img.shape[0] == 0 or img.shape[1] == 0 :
                pass
                
            else :
                img = cv2.resize(img, (48, 48))
                img = np.expand_dims(img, axis=0)
                img = img / 255.0  # Normalize the image

                emotion_preds = model.predict(img)
                prediction_index = emotion_preds[0].argmax()

                percentage = emotion_preds[0][prediction_index]
                label = emotion_labels[prediction_index]
                return [label, percentage*100]

def get_emotion_predictions_from_base64_image(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    face_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    try:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    except:
        pass

    rects = detector(face_img , 0)
    if len(rects) >= 1 :
        for rect in rects :
            (x , y , w , h) = rect_to_bb(rect)
            img = face_img[y-10 : y+h+10 , x-10 : x+w+10]

            if img.shape[0] == 0 or img.shape[1] == 0 :
                pass
                
            else :
                img = cv2.resize(img, (48, 48))
                img = np.expand_dims(img, axis=0)
                img = img / 255.0  # Normalize the image

                emotion_preds = model.predict(img)
                prediction_index = emotion_preds[0].argmax()

                percentage = emotion_preds[0][prediction_index]
                label = emotion_labels[prediction_index]
                return [label, percentage*100]


