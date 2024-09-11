import cv2
import curses
from app.regular_mode import RegularAsciiArtGenerator
from app.ai_mode import AiasciiArtGenerator


class LiveAsciiTUI:
    
    def __init__(self, cam_index=0, conversion_size=1):
    
        self.cam_index = cam_index
        self.cap = None
        self.conversion_size = conversion_size
        self.regular_mode_ascii_art_generator = RegularAsciiArtGenerator().convert_frame_to_ascii
        self.ai_mode_ascii_art_generator = AiasciiArtGenerator().convert_frame_to_ascii
        self.mode = 'REGULAR'
        
    
    def start_capture(self, stdscr):
        
        self.setup_curses(stdscr)
        self.initialize_capture()

        while True:
            max_y, max_x = stdscr.getmaxyx()
            ret, frame = self.capture_frame(stdscr)
            if not ret:
                break

            ascii_art = self.generate_ascii(frame, max_x, max_y)
            self.render_ascii_art(stdscr, ascii_art, max_x, max_y)
            
            key = stdscr.getch()
            if self.handle_keypress(key):
                break

        self.cap.release()
        

    def setup_curses(self, stdscr):
    
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.nodelay(True)
        

    def initialize_capture(self):
       
        self.cap = cv2.VideoCapture(self.cam_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open webcam.")

    
    def capture_frame(self, stdscr):
        
        ret, frame = self.cap.read()
        
        if not ret:
            stdscr.addstr(1, 0, "Failed to grab frame.", curses.color_pair(1))
            stdscr.refresh()
        
        return ret, cv2.flip(frame, 1)

    
    def generate_ascii(self, frame, max_x, max_y):

        resize_frame = cv2.resize(frame, (max_x, max_y))

        return self.regular_mode_ascii_art_generator(resize_frame) if self.mode == 'REGULAR' else self.ai_mode_ascii_art_generator(resize_frame)



    def render_ascii_art(self, stdscr, ascii_art, max_x, max_y):

        title_text = f'LIVE ASCII ART ({self.mode} mode)'
        change_mode_text = f"To change mode to {'AI' if self.mode == 'REGULAR' else 'REGULAR'}, press 'c'."
        
        vertical_offset = 4
        limited_ascii = '\n'.join(line[:max_x] for line in ascii_art.split('\n')[:max_y-vertical_offset-1])
        ascii_lines = limited_ascii.split('\n')
        
        stdscr.clear()
        stdscr.addstr(0, 0, 'Press q to close.', curses.color_pair(1))
        stdscr.addstr(1, (max_x-len(title_text))//2, title_text, curses.color_pair(2))
        stdscr.addstr(2, (max_x-len(change_mode_text))//2, change_mode_text, curses.color_pair(2))

        for i, line in enumerate(ascii_lines):
            stdscr.addstr(vertical_offset+i, (max_x - len(line))//2, line, curses.color_pair(1))
        
        stdscr.refresh()

    
    def handle_keypress(self, key):
    
        if key == ord('q'):
            return True
        
        elif key == ord('c'):
            self.change_mode()

        return False


    def change_mode(self):

        self.mode = 'AI' if self.mode == 'REGULAR' else 'REGULAR'
