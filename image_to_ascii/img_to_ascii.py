class Image2Ascii:
    '''
    This is a typical implementation of image to Ascii art (to a text format output).
    It takes approximately less than a 0.1s (0.072 in average over 100 run).
    '''
    
    def __init__(self, ascii_chars=None, conversion_size=None):
        
        self.ASCII_CHARS = ascii_chars or ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        self.conversion_size = conversion_size
        self.new_width = None
        self.new_height = None
        
        
    def resize_image(self, image):
        """Resize the image to a new width while maintaining aspect ratio."""
        img_width, img_height = image.size
        
        self.new_width = int(img_width // self.conversion_size)
        self.new_height = int(img_height // self.conversion_size)
        
        image = image.resize((self.new_width, self.new_height))
        
        return image


    def grayscale_image(self, image):
        """Convert the image to grayscale."""
        return image.convert("L")    
        

    def map_pixel_to_ascii(self, image):
        
        pixels = image.getdata()
        ascii_str = ""
        
        for pixel_value in pixels:
            ascii_index = int((pixel_value / 255) * (len(self.ASCII_CHARS) - 1))
            ascii_str += self.ASCII_CHARS[ascii_index]
            
        ascii_art = "\n".join([ascii_str[i: i+self.new_width] for i in range(0, len(ascii_str), self.new_width)])
        
        return ascii_art
    
    
    def convert_image_to_ascii(self, image):
        
        resized_image = self.resize_image(image)
        gray_image = self.grayscale_image(resized_image)
        ascii_art = self.map_pixel_to_ascii(gray_image)
        
        return ascii_art   
        
        
    def calc_avg_run_time(self, image):
        import time
        
        avg_run_time = 0
        times = 10
        
        for i in range(times):
            start = time.time()
            self.convert_image_to_ascii(image)
            end = time.time()
            avg_run_time += (end - start)
            
        print(f'average run-time over {times} running = ', avg_run_time / times)
        
        return avg_run_time

