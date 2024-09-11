import cv2
import numpy as np
from PIL import Image, ImageFont
from matplotlib import cm
import matplotlib.pyplot as plt 

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_to_ascii.img_to_ascii import Image2Ascii
from image_to_ascii.ascii_srt_to_ascii_img import AsciiStr2AsciiImg
import os

class LiveAsciiApp:
    def __init__(self, cam_index=0, width=640, font_path=None, font_size=10, conversion_size=5):
        
        self.cam_index = cam_index
        self.width = width
        self.font_size = font_size
        self.cap = None
        self.conversion_size = conversion_size
        
        
        self.font_size = font_size
        #self.font_path = font_path or os.path.join(os.path.dirname(__file__), 'fonts/consola.ttf')
        #self.font = ImageFont.truetype(self.font_path, self.font_size)
        self.font = ImageFont.load_default()
        

    def start_capture(self):
        """Start capturing from the webcam and display ASCII images."""
        # Start capturing video from the webcam
        self.cap = cv2.VideoCapture(self.cam_index)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        print("Press 'q' to quit.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            '''
            # Get the size of the current window
            window_size = cv2.getWindowImageRect('ASCII Art Window')
            window_width = window_size[2]  # Current window width
            window_height = window_size[3]  # Current window height
            
            # Resize the ASCII image to half the window's current size
            half_window_width = window_width // 2
            half_window_height = window_height
            '''
            mirrored_frame = cv2.flip(frame, 1)
            frame_width, frame_height = mirrored_frame.shape[0], mirrored_frame.shape[1] 
            
            #resized_frame = cv2.resize(mirrored_frame, (self.width * 2, int(self.width * 2 * (mirrored_frame.shape[0] / mirrored_frame.shape[1]))))
            #grayscale_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

            # Regular ASCII art conversion (Left half of the window)
            ascii_art = self.convert_frame_to_ascii(mirrored_frame)
            ascii_art = cv2.resize(ascii_art, (frame_width, frame_height))

            # AI-based ASCII art conversion (Right half of the window - Placeholder for now)
            #ai_ascii_art = self.convert_frame_to_ai_ascii(grayscale_frame)

            # Combine both ASCII arts side by side
            #combined_ascii = self.combine_ascii(ascii_art, ai_ascii_art)
            
            # Convert the ASCII text to an image and display it in a window
            #ascii_img = self.ascii_to_image(ascii_art)        

            #resized_ascii_img = cv2.resize(ascii_art)

            cv2.imshow('ASCII Art Window', ascii_art)

            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or cv2.getWindowProperty('ASCII Art Window', cv2.WND_PROP_VISIBLE) < 1:
                break
            '''
            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit when 'q' is pressed
                break
            elif key == 2490368:  # Up arrow key
                self.conversion_size = min(40, self.conversion_size + 5)
                print(f"Conversion size increased to {self.conversion_size}")
            elif key == 2621440:  # Down arrow key
                self.conversion_size = max(5, self.conversion_size - 5)
                print(f"Conversion size decreased to {self.conversion_size}")
                
            '''    
        # Release the webcam
        self.cap.release()

    def convert_frame_to_ascii(self, frame):
        """Convert a grayscale frame to ASCII using the regular method."""
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        image2Ascii = Image2Ascii(conversion_size=self.conversion_size)

        ascii_art = image2Ascii.convert_image_to_ascii(img)
        
        str2img = AsciiStr2AsciiImg(self.font)
        
        return str2img.convert_str_ascii_art_2_img(ascii_art)

    def convert_frame_to_ai_ascii(self, frame):
        """
        Convert a grayscale frame to ASCII using an AI-based method.
        Placeholder method for AI-based conversion.
        """
        # Placeholder for future AI-based ASCII conversion logic
        placeholder_ascii = "AI-based ASCII Conversion (Not Implemented Yet)\n" * 10
        return placeholder_ascii

    def combine_ascii(self, ascii_art_left, ascii_art_right):
        """
        Combine two ASCII art strings side by side.
        
        Parameters:
        - ascii_art_left: The left ASCII art (regular).
        - ascii_art_right: The right ASCII art (AI-based, placeholder).
        
        Returns:
        A combined ASCII art string with both side by side.
        """
        left_lines = ascii_art_left.split('\n')
        right_lines = ascii_art_right.split('\n')

        combined = ""
        for left, right in zip(left_lines, right_lines):
            combined += left + "   |   " + right + "\n"

        return combined

# Example usage
if __name__ == "__main__":
    app = LiveAsciiApp()
    app.start_capture()
