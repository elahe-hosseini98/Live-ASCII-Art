import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from config import celeba_ds_path, ascii_art_ds_path, target_dataset_input_size, ASCII_CHARS

class DataLoader:
   
    def __init__(self, img_dir=None, ascii_dir=None, test_size=0.2, random_state=42):
     
        self.img_dir = img_dir or celeba_ds_path
        self.ascii_dir = ascii_dir or ascii_art_ds_path
        self.random_state = random_state

        self.img_names = sorted(os.listdir(self.img_dir))[:1000]
        self.ascii_names = sorted(os.listdir(self.ascii_dir))[:1000]

        self.img_train, self.img_val, self.ascii_train, self.ascii_val = train_test_split(
            self.img_names, self.ascii_names, test_size=test_size, random_state=random_state
        )
        

    def _load_image(self, img_path):
        """Load and preprocess the image."""
      
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, target_dataset_input_size) 
        image = image / 255.0  
        image = np.expand_dims(image, axis=-1)
        
        return image
    

    def _char_to_one_hot(self, char):
        """Convert a single ASCII character to one-hot encoded vector."""
    
        one_hot = np.zeros(len(ASCII_CHARS))
        
        if char in ASCII_CHARS:
            index = ASCII_CHARS.index(char)
            one_hot[index] = 1
        
        return one_hot
    

    def _load_ascii(self, ascii_path):
        """Load ASCII art, convert strings to 3D one-hot encoded array."""
      
        with open(ascii_path, 'r') as file:
            ascii_art = file.readlines()  
        ascii_art_one_hot = np.array([[self._char_to_one_hot(char) for char in row.strip()] for row in ascii_art])
        
        return ascii_art_one_hot

    
    def data_generator(self, img_list, ascii_list):
        """Generator that yields single samples of image and ASCII data."""
    
        while True:
            for img_name, ascii_name in zip(img_list, ascii_list):
                if isinstance(img_name, bytes):
                    img_name = img_name.decode('utf-8')
                if isinstance(ascii_name, bytes):
                    ascii_name = ascii_name.decode('utf-8')
    
                img_path = os.path.join(self.img_dir, img_name)
                ascii_path = os.path.join(self.ascii_dir, ascii_name)

                X = self._load_image(img_path)
                y = self._load_ascii(ascii_path)
    
                yield np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

    
    def create_tf_dataset(self, batch_size, is_training=True):
        """Create a TensorFlow Dataset for training or validation."""
        img_list = self.img_train if is_training else self.img_val
        ascii_list = self.ascii_train if is_training else self.ascii_val
    
        dataset = tf.data.Dataset.from_generator(
            lambda: self.data_generator(img_list, ascii_list),
            output_types=(tf.float32, tf.float32),
            output_shapes=((128, 128, 1), (128, 128, len(ASCII_CHARS)))  # Single sample, no batch size
        )
        
        dataset = dataset.batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)
        return dataset

    