from image_to_ascii.img_to_ascii import Image2Ascii
from PIL import Image
import cv2


class RegularAsciiArtGenerator():
    
    def __init__(self, conversion_size=1):
        self.conversion_size = conversion_size
        
    def convert_frame_to_ascii(self, frame):
        
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image2Ascii = Image2Ascii(conversion_size=self.conversion_size)
        ascii_art = image2Ascii.convert_image_to_ascii(frame)
        
        return ascii_art
    
    