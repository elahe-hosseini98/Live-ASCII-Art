import h5py
import numpy as np
import os
import cv2
from config import ASCII_CHARS, saved_hdf5_full_path, celeba_ds_path, ascii_art_ds_path


class CreateHDF5:
    
    def __init__(self, img_dir=None, ascii_dir=None, img_names=None, ascii_names=None, hdf5_full_path=None, img_shape=(128, 128)):
        self.img_dir = img_dir or celeba_ds_path
        self.ascii_dir = ascii_dir or ascii_art_ds_path
        self.img_names = sorted(os.listdir(self.img_dir))
        self.ascii_names = sorted(os.listdir(self.ascii_dir))
        self.img_shape = img_shape
        self.hdf5_full_path = hdf5_full_path or saved_hdf5_full_path


    def _char_to_one_hot(self, char):
        """Convert a single ASCII character to one-hot encoded vector."""
        
        one_hot = np.zeros(len(ASCII_CHARS))
        if char in ASCII_CHARS:
            index = ASCII_CHARS.index(char)
            one_hot[index] = 1
        return one_hot
    
    
    def create_hdf5(self):
        
        num_samples = len(self.img_names)
        
        with h5py.File(self.hdf5_full_path, 'w') as hf:
           
            hf.create_dataset('images', shape=(num_samples, *self.img_shape, 1), dtype=np.float32)
            hf.create_dataset('ascii_art', shape=(num_samples, *self.img_shape, len(ASCII_CHARS)), dtype=np.float32)
            
            for i, (self.img_name, self.ascii_name) in enumerate(zip(self.img_names, self.ascii_names)):

                img_path = os.path.join(self.img_dir, self.img_name)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                image = cv2.resize(image, self.img_shape) / 255.0
                image = np.expand_dims(image, axis=-1)  # Add the channel dimension (128, 128, 1)
            
                
                ascii_path = os.path.join(self.ascii_dir, self.ascii_name)
                with open(ascii_path, 'r') as file:
                    ascii_art = file.readlines()
                ascii_art_one_hot = np.array([[self._char_to_one_hot(char) for char in row.strip()] for row in ascii_art])
                
                hf['images'][i] = image
                hf['ascii_art'][i] = ascii_art_one_hot
    
                # Print progress every 1000 samples
                if (i + 1) % 100 == 0:
                    print(f'Processed {i + 1}/{num_samples} samples')
                    
                    
                    
                    
                    