import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split  
import os
import cv2
# from google.colab.patches import cv2_imshow
# import matplotlib.pyplot as plt
# from tensorflow.keras.layers import Dropout
# from tensorflow.keras.layers import Flatten,BatchNormalization
# from tensorflow.keras.layers import Dense, MaxPooling2D,Conv2D
# from tensorflow.keras.layers import Input,Activation,Add
# from tensorflow.keras.models import Model
# from tensorflow.keras.regularizers import l2
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import ModelCheckpoint
# import pandas as pd
# from keras.models import Sequential,load_model,Model
# from keras.layers import Conv2D,MaxPool2D,Dense,Dropout,BatchNormalization,Flatten,Input
# from sklearn.model_selection import train_test_split


dataset_folder='./input/CK+48'
sub_folders=os.listdir(dataset_folder)

i=0
last=[]
images=[]
labels=[]
temp = sub_folders

for sub_folder in sub_folders:
    sub_folder_index = temp.index(sub_folder)
    label = sub_folder_index
    path = dataset_folder+'/'+sub_folder
    sub_folder_images= os.listdir(path)

    for image in sub_folder_images:
        image_path = path+'/'+image
        print(image_path+"\t"+str(label))
        image = cv2.imread(image_path) #read image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image,(48,48))
        images.append(image)
        labels.append(label)
        i+=1

    last.append(i)

# Declare x and y  
images_x = np.array(images)
labels_y = np.array(labels)

# We divide image pixels by 255 to reduce computation power
images_x = images_x/255

# encoding the labels
num_of_classes = 7
labels_y_encoded = tf.keras.utils.to_categorical(labels_y,num_classes=num_of_classes)

# Split into 75:25 train and test
X_train, X_test, Y_train, Y_test= train_test_split(images_x, labels_y_encoded,test_size=0.25, random_state=10)