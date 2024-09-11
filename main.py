import curses
from app.tui import LiveAsciiTUI

if __name__ == "__main__":
    tui = LiveAsciiTUI()
    curses.wrapper(tui.start_capture)