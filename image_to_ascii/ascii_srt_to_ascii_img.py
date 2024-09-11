from PIL import Image, ImageDraw
import numpy as np

class AsciiStr2AsciiImg:
    '''
    This is a typical implementation of image to Ascii art (to a text format output).
    It takes approximately less than a 0.1s (0.072 in average over 100 run).
    '''
    
    def __init__(self, font=None):
        self.font = font
    
    def convert_str_ascii_art_2_img(self, ascii_art):
        ascii_lines = ascii_art.split('\n')[:-1]
        
        # Set up image size based on the number of lines and characters per line
        char_width, char_height = self.font.getsize("A")
        img_height = len(ascii_lines) * char_height
        img_width = len(ascii_lines[0]) * char_width
        
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)
        
        for y, line in enumerate(ascii_lines):
            draw.text((0, y * char_height), line, font=self.font, fill="black")
        
        return np.array(image)