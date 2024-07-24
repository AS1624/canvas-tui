import curses
import time
import sys
import readchar

def putChar(x: int, y: int, char: chr, bold: bool = False, italics: bool = False, underline: bool = False, header: bool = False, inverse: bool = False, color: int = 0) -> None:
    height, width = window.getmaxyx()

    if(x >= 0 and x < width and y >= 0 and y < height):
        attr = (
                bold * curses.A_BOLD
              + italics * curses.A_ITALIC
              + underline * curses.A_UNDERLINE
              + inverse * curses.A_REVERSE
              + curses.color_pair(color)
               )
        if header:
            attr = curses.A_BOLD + curses.A_UNDERLINE + curses.color_pair(3)
        window.move(y, x)
        window.echochar(char, attr)

def clear() -> None:
    window.clear()

def readBuffer() -> chr:
    value = readchar.readchar()
    return value

def charCode(char: chr) -> int:
        for i in range(256):
            if chr(i) == char:
                return i

def test(win: curses.window):
    h, w= win.getmaxyx()
    global window 
    global width
    global height

    window = win
    width = w
    height = h
    curses.curs_set(0)

    for i in range(20):
        putChar(i, i, chr(i + 64), underscore = True)

    while True:
        putChar(20, 0, readBuffer(), True, True, True)

    time.sleep(7)

def start(win, fun):
    h, w =  win.getmaxyx()
    global window 
    global width
    global height

    window = win
    width = w
    height = h

    curses.curs_set(0)
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    fun(win)

def init(fun: callable):
    curses.wrapper(start, fun)

if __name__ == "__main__":
    curses.wrapper(test)
    
