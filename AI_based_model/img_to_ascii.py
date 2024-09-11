from config import saved_model_path, target_dataset_input_size, ASCII_CHARS
from tensorflow.keras.models import load_model
import numpy as np
import cv2


class Image2Ascii:
    
    def __init__(self, model_dir=None, model_name='best_performing_model.h5'):
        self.model_dir = model_dir or saved_model_path
        self.model_name = model_name
        self.model = self._load_model()
        
    
    def _load_model(self):
        """Load the saved model."""
        model_path = f"{self.model_dir}/{self.model_name}"
        try:
            model = load_model(model_path)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
        return model
    
    
    def _fix_ascii_art_format(self, ascii_art):
        """
        Convert the predicted ASCII art (2D array) back to a readable string format.
        Each row of the ASCII art should be joined and printed row by row.
        """
        ascii_art_str = "\n".join(["".join(row) for row in ascii_art])
        
        return ascii_art_str
    
    
    def _preprocess_image(self, image):
        """
        Preprocess the input image (resize, grayscale, normalize) to fit the model's expected input.
        """
        target_size = target_dataset_input_size

        if (image.shape[0], image.shape[1]) != target_size:
            image = cv2.resize(image, target_size)
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = np.expand_dims(image, axis=-1)  
        image = image / 255.0  
        image = np.expand_dims(image, axis=0) 
        
        return image
    
    
    def _one_hot_to_ascii(self, prediction):
        """
        Convert the model's one-hot encoded output back to ASCII characters.
        Assumes the ASCII_CHARS are stored in config.py.
        """
        
        ascii_art = []
        
        for row in prediction:
            ascii_row = [ASCII_CHARS[np.argmax(pixel)] for pixel in row]
            ascii_art.append(ascii_row)
        
        return ascii_art

    
    def convert_image_to_ascii(self, image):
        """
        Convert the input image to ASCII art by passing it through the model and interpreting the output.
        """
        
        if self.model is None:
            print("Model not loaded.")
            return None
        
        processed_image = self._preprocess_image(image)
        
        ascii_prediction = self.model.predict(processed_image)
        
        ascii_art = self._one_hot_to_ascii(ascii_prediction[0])

        ascii_art_str = self._fix_ascii_art_format(ascii_art)
        
        return ascii_art_str
    
   