import cv2
import numpy as np
import tensorflow as tf
import base64
from PIL import Image
import io
import codecs


emotion_labels = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']

model = tf.keras.models.load_model('./output/emotion_model_pretrained.keras')

def get_emotion_predictions(face_img):
    face_img = cv2.imread(face_img, cv2.COLOR_BGR2GRAY)
    face_img = cv2.resize(face_img, (48, 48))
    face_img = np.expand_dims(face_img, axis=0)
    face_img = face_img / 255.0  # Normalize the image

    emotion_preds = model.predict(face_img)
    prediction_index = emotion_preds[0].argmax()

    percentage = emotion_preds[0][prediction_index]
    label = emotion_labels[prediction_index]
    return [label, percentage*100]

def get_emotion_predictions_from_base64_image(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    face_img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
    face_img = cv2.resize(face_img, (48, 48))
    face_img = np.expand_dims(face_img, axis=0)
    face_img = face_img / 255.0  # Normalize the image

    emotion_preds = model.predict(face_img)
    prediction_index = emotion_preds[0].argmax()

    percentage = emotion_preds[0][prediction_index]
    label = emotion_labels[prediction_index]
    return [label, percentage*100]
