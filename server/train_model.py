import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense, MaxPooling2D,Conv2D
from tensorflow.keras.layers import Input,Activation
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ModelCheckpoint

from keras.models import Model
from keras.layers import Conv2D,Dense,Dropout,Flatten,Input
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split 


# data set folder should not have any other files or folder than the classes and data sets
# assuming number of folders in dataset_folder equals to number of classes
def read_datasets(dataset_folder):
    images=[]
    labels=[]

    sub_folders=os.listdir(dataset_folder)
    num_classes = len(sub_folders)

    for sub_folder_index, sub_folder in enumerate(sub_folders):
        label = sub_folder_index
        path = dataset_folder+'/'+sub_folder
        sub_folder_images= os.listdir(path)

        for image in sub_folder_images:
            image_path = path+'/'+image
            image = cv2.imread(image_path) #read image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image,(48,48))
            images.append(image)
            labels.append(label)

    return [images, labels, num_classes]



def pre_process_data(images, labels):
    
    # Declare x and y
    images_x = np.array(images)
    labels_y = np.array(labels)
    
    # divide image pixels by 255 to reduce computation power
    images_x = images_x/255

    # encoding the labels
    num_of_classes = 7
    labels_y_encoded = tf.keras.utils.to_categorical(labels_y, num_classes=num_of_classes)

    return train_test_split(images_x, labels_y_encoded,test_size=0.25, random_state=10)



# CNN Architecture
def cnn_architecture(num_classes):
    input = Input(shape = (48,48,1))
    conv1 = Conv2D(32,(3, 3), padding = 'same', strides=(1, 1), kernel_regularizer=l2(0.001))(input)
    conv1 = Dropout(0.1)(conv1)
    conv1 = Activation('relu')(conv1)
    pool1 = MaxPooling2D(pool_size = (2,2)) (conv1)
    conv2 = Conv2D(64,(3, 3), padding = 'same', strides=(1, 1), kernel_regularizer=l2(0.001))(pool1)
    conv2 = Dropout(0.1)(conv2)
    conv2 = Activation('relu')(conv2)
    pool2 = MaxPooling2D(pool_size = (2,2)) (conv2)
    conv3 = Conv2D(128,(3, 3), padding = 'same', strides=(1, 1), kernel_regularizer=l2(0.001))(pool2)
    conv3 = Dropout(0.1)(conv3)
    conv3 = Activation('relu')(conv3)
    pool3 = MaxPooling2D(pool_size = (2,2)) (conv3)
    conv4 = Conv2D(256,(3, 3), padding = 'same', strides=(1, 1), kernel_regularizer=l2(0.001))(pool3)
    conv4 = Dropout(0.1)(conv4)
    conv4 = Activation('relu')(conv4)
    pool4 = MaxPooling2D(pool_size = (2,2)) (conv4)
    flatten = Flatten()(pool4)
    dense_1 = Dense(128,activation='relu')(flatten)
    drop_1 = Dropout(0.2)(dense_1)
    output = Dense(num_classes,activation="sigmoid")(drop_1)
    return [input, output]


def train_model():
    images, labels, num_classes = read_datasets('./input/CK+48')
    X_train, X_test, Y_train, Y_test = pre_process_data(images, labels)
    input, output = cnn_architecture(num_classes)

    # Model compile
    model = Model(inputs=input,outputs=output)
    model.compile(optimizer="adam", loss=["categorical_crossentropy"], metrics=['accuracy'])
    model.summary()

    # Configure Model Checkpoint
    fle_s='./output/emotion_model.keras'
    checkpointer = ModelCheckpoint(fle_s, monitor='loss',verbose=1,save_best_only=True,
                                save_weights_only=False, mode='auto',save_freq='epoch')
    callback_list=[checkpointer]

    model.fit(X_train,Y_train,batch_size=32,validation_data=(X_test,Y_test),epochs=50,callbacks=[callback_list])
    model.save('./output/emotion_model_pretrained.keras')


train_model()

