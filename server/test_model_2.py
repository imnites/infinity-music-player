import tensorflow as tf
import numpy as np
import cv2

import dlib
import pickle
import base64

# import efficientnet.tfkeras as efn
from tensorflow.keras.models import load_model


import tensorflow as tf
print(tf.__version__)

model = load_model("FacialExpressionModel.keras")

def load_object(name):
    pickle_obj = open(f"{name}.pck","rb")
    obj = pickle.load(pickle_obj)
    return obj

Le = load_object("LabelEncoder")

def ProcessImage(image):
    image = tf.convert_to_tensor(image)
    image = tf.image.resize(image , [96 , 96] , method="bilinear")
    image = tf.expand_dims(image , 0)
    return image

def RealtimePrediction(image , model, encoder_):
    prediction = model.predict(image)
    print(prediction)
    prediction = np.argmax(prediction , axis = 1)
    return encoder_.inverse_transform(prediction)

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


VideoCapture = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()


def predict_label(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    face_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    except:
        pass

    rects = detector(face_img , 0)
    print(len(rects))
    if len(rects) >= 1 :
        for rect in rects :
            (x , y , w , h) = rect_to_bb(rect)
            img = face_img[y-10 : y+h+10 , x-10 : x+w+10]

            if img.shape[0] == 0 or img.shape[1] == 0 :
                pass
                
            else :
                img = cv2.cvtColor(img , cv2.COLOR_GRAY2RGB)
                img = ProcessImage(img)
                out = RealtimePrediction(img , model , Le)
                print(out)
