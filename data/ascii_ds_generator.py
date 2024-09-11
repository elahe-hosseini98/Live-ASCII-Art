import os
import cv2
from app.regular_mode import RegularAsciiArtGenerator
from config import celeba_ds_path, ascii_art_ds_path, target_dataset_input_size


class AsciiArtDatasetGenerator:
    
    def __init__(self, image_folder=None, ascii_output_folder=None):
    
        self.image_folder = image_folder or celeba_ds_path
        self.ascii_output_folder = ascii_output_folder or ascii_art_ds_path
        self.ascii_art_generator = RegularAsciiArtGenerator(conversion_size=1)
        

    def ascii_art_ds_generator(self):
        
        for img_name in os.listdir(self.image_folder):
            img_path = os.path.join(self.image_folder, img_name)

            try:
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, target_dataset_input_size) 
                
                # Convert the image to ASCII
                ascii_art = self.ascii_art_generator.convert_frame_to_ascii(img)  
                
                # Save the ASCII art, as a .txt file
                ascii_file_path = os.path.join(self.ascii_output_folder, f"{os.path.splitext(img_name)[0]}.txt")
                with open(ascii_file_path, 'w') as f:
                    f.write(ascii_art)
                    
                print(f"Processed and saved ASCII art for {img_name}")
           
            except Exception as e:
                print(f"Failed to process {img_name}: {e}")
