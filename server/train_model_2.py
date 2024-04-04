import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split 
from tensorflow.keras.applications import EfficientNetB2
import pickle

tf.random.set_seed(4)

def read_images_path(dataset_folder):
    imagesPath=[]
    sub_folders = os.listdir(dataset_folder)

    for sub_folder in sub_folders:
        path = dataset_folder+'/'+sub_folder
        sub_folder_images= os.listdir(path)

        for image in sub_folder_images:
            imagesPath.append(path+'/'+image)

    return imagesPath

train_image_paths = read_images_path('./content/train')

def get_label(image_path):
    return image_path.split("/")[-2]

train_image_labels = list(map(lambda x : get_label(x) , train_image_paths))

Le = LabelEncoder()
train_image_labels = Le.fit_transform(train_image_labels)

train_image_labels = tf.keras.utils.to_categorical(train_image_labels)

Train_paths , Val_paths , Train_labels , Val_labels = train_test_split(train_image_paths , train_image_labels , test_size = 0.25)

classTotals = Train_labels.sum(axis=0)
classWeight = classTotals.max() / classTotals

class_weight = {e : weight for e , weight in enumerate(classWeight)}
print(class_weight)

def load(image , label):
    image = tf.io.read_file(image)
    image = tf.io.decode_jpeg(image , channels = 3)
    return image , label



IMG_SIZE = 96 
BATCH_SIZE = 32

# Basic Transformation
resize = tf.keras.Sequential([
    tf.keras.layers.Resizing(IMG_SIZE, IMG_SIZE)          
])

# Data Augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(height_factor = (-0.1, -0.05))
])


AUTOTUNE = tf.data.experimental.AUTOTUNE
def get_dataset(paths , labels , train = True):
    image_paths = tf.convert_to_tensor(paths)
    labels = tf.convert_to_tensor(labels)

    image_dataset = tf.data.Dataset.from_tensor_slices(image_paths)
    label_dataset = tf.data.Dataset.from_tensor_slices(labels)

    dataset = tf.data.Dataset.zip((image_dataset , label_dataset))

    dataset = dataset.map(lambda image , label : load(image , label))
    dataset = dataset.map(lambda image, label: (resize(image), label) , num_parallel_calls=AUTOTUNE)
    dataset = dataset.shuffle(1000)
    dataset = dataset.batch(BATCH_SIZE)

    if train:
        dataset = dataset.map(lambda image, label: (data_augmentation(image), label) , num_parallel_calls=AUTOTUNE)
    
    dataset = dataset.repeat()
    print(dataset)
    return dataset


train_dataset = get_dataset(Train_paths , Train_labels)

image , label = next(iter(train_dataset))
print(image.shape)
print(label.shape)

print(Le.inverse_transform(np.argmax(label , axis = 1))[0])
plt.imshow((image[0].numpy()/255).reshape(96 , 96 , 3))

val_dataset = get_dataset(Val_paths , Val_labels , train = False)

image , label = next(iter(val_dataset))
print(image.shape)
print(label.shape)


print(Le.inverse_transform(np.argmax(label , axis = 1))[0])
plt.imshow((image[0].numpy()/255).reshape(96 , 96 , 3))



backbone = EfficientNetB2(
    input_shape=(96, 96, 3),
    include_top=False
)

model = tf.keras.Sequential([
    backbone,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(7, activation='softmax')
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07),
    loss = 'categorical_crossentropy',
    metrics=['accuracy' , tf.keras.metrics.Precision(name='precision'),tf.keras.metrics.Recall(name='recall')]
)

history = model.fit(
    train_dataset,
    steps_per_epoch=len(Train_paths)//BATCH_SIZE,
    epochs=12,
    validation_data=val_dataset,
    validation_steps = len(Val_paths)//BATCH_SIZE,
    class_weight=class_weight
)

model.layers[0].trainable = False

checkpoint = tf.keras.callbacks.ModelCheckpoint("custom.keras",verbose=1,save_best_only=True,save_weights_only=False, mode='auto',save_freq='epoch')
early_stop = tf.keras.callbacks.EarlyStopping(patience=4)

model.summary()

history = model.fit(
    train_dataset,
    steps_per_epoch=len(Train_paths)//BATCH_SIZE,
    epochs=8,
    callbacks=[checkpoint , early_stop],
    validation_data=val_dataset,
    validation_steps = len(Val_paths)//BATCH_SIZE,
    class_weight=class_weight
)

backbone = EfficientNetB2(
    input_shape=(96, 96, 3),
    include_top=False
)

model = tf.keras.Sequential([
    backbone,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(7, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07),
    loss = 'categorical_crossentropy',
    metrics=['accuracy' , tf.keras.metrics.Precision(name='precision'),tf.keras.metrics.Recall(name='recall')]
)

# model.load_weights("custom.keras")

# test_image_paths = read_images_path('./content/test')
# test_image_paths = list(map(lambda x : str(x) , test_image_paths))
# test_labels = list(map(lambda x : get_label(x) , test_image_paths))

# test_labels = Le.transform(test_labels)
# test_labels = tf.keras.utils.to_categorical(test_labels)

# test_image_paths = tf.convert_to_tensor(test_image_paths)
# test_labels = tf.convert_to_tensor(test_labels)

# def decode_image(image , label):
#     image = tf.io.read_file(image)
#     image = tf.io.decode_jpeg(image , channels = 3)
#     image = tf.image.resize(image , [96 , 96] , method="bilinear")
#     return image , label

# test_dataset = (
#      tf.data.Dataset
#     .from_tensor_slices((test_image_paths, test_labels))
#     .map(decode_image)
#     .batch(BATCH_SIZE)
# )

# image , label = next(iter(test_dataset))
# print(image.shape)
# print(label.shape)

# print(Le.inverse_transform(np.argmax(label , axis = 1))[0])
# plt.imshow((image[0].numpy()/255).reshape(96 , 96 , 3))

# loss, acc, prec, rec = model.evaluate(test_dataset)

# print(" Testing Acc : " , acc)
# print(" Testing Precision " , prec)
# print(" Testing Recall " , rec)
model.build()
model.save("FacialExpressionModel.keras")

def save_object(obj , name):
    pickle_obj = open(f"{name}.pck","wb")
    pickle.dump(obj, pickle_obj)
    pickle_obj.close()


save_object(Le, "LabelEncoder")