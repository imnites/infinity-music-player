import streamlit as st
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import base64


model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
holis = holistic.Holistic()

def predict_result(frm):
    
    res = holis.process(frm)

    lst = []

    if res.face_landmarks:
        for i in res.face_landmarks.landmark:
            lst.append(i.x - res.face_landmarks.landmark[1].x)
            lst.append(i.y - res.face_landmarks.landmark[1].y)

        if res.left_hand_landmarks:
            for i in res.left_hand_landmarks.landmark:
                lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)

        if res.right_hand_landmarks:
            for i in res.right_hand_landmarks.landmark:
                lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
        else:
            for i in range(42):
                lst.append(0.0)

        lst = np.array(lst).reshape(1,-1)

        pred = label[np.argmax(model.predict(lst))]

        return pred

def get_emotion_predictions_from_base64_image(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    face_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    try:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    except:
        pass

    return predict_result(face_img)