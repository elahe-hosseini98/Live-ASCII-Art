from AI_based_model.img_to_ascii import Image2Ascii

class AiasciiArtGenerator():
        
    def convert_frame_to_ascii(self, frame):
        
        image2Ascii = Image2Ascii()
        ascii_art = image2Ascii.convert_image_to_ascii(frame)
        
        return ascii_art
    
    