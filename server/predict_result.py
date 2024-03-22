import cv2
import numpy as np
import tensorflow as tf


emotion_labels = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']

model = tf.keras.models.load_model('./output/emotion_model_pretrained.keras')

def get_emotion_predictions(face_img):
    face_img = cv2.imread(face_img, cv2.COLOR_BGR2GRAY)
    face_img = cv2.resize(face_img, (48, 48))
    face_img = np.expand_dims(face_img, axis=0)
    face_img = face_img / 255.0  # Normalize the image

    emotion_preds = model.predict(face_img)
    prediction_index = emotion_preds[0].argmax()
    return emotion_labels[prediction_index]

emotion_preds = get_emotion_predictions('S010_004_00000017.png')
print(emotion_preds)