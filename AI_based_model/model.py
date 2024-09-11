import tensorflow as tf
from tensorflow.keras import layers, models

def build_cnn_model(ascii_height, ascii_width, num_classes):
    
    model = models.Sequential()

    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    
    model.add(layers.Dense(ascii_height * ascii_width * num_classes, activation='softmax'))
    
    model.add(layers.Reshape((ascii_height, ascii_width, num_classes)))

    return model
