import sys
import time
import tkinter

_root_window = None
_canvas = None
_window_closed = False

def formatColor(r, g, b):
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))

def sleep(secs):
    global _root_window, _window_closed
    if _root_window is None:
        time.sleep(secs)
    else:
        end = time.time() + secs
        while time.time() < end:
            try:
                _root_window.update()
            except:
                _window_closed = True
                break
            time.sleep(0.01)

def begin_graphics(width, height, color=formatColor(0, 0, 0), title="Pacman"):
    global _root_window, _canvas, _window_closed
    if _root_window: _root_window.destroy()
    
    _root_window = tkinter.Tk()
    _root_window.title(title)
    _root_window.resizable(0, 0)
    _root_window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    
    _canvas = tkinter.Canvas(_root_window, width=width, height=height, bg=color, highlightthickness=0)
    _canvas.pack()
    _window_closed = False

def circle(pos, r, outlineColor, fillColor, endpoints=None, width=2):
    x, y = pos
    x0, x1 = x - r, x + r
    y0, y1 = y - r, y + r
    if endpoints is None:
        e = [0, 359]
    else:
        e = list(endpoints)
    while e[0] > e[1]: e[1] += 360

    return _canvas.create_arc(x0, y0, x1, y1, outline=outlineColor, fill=fillColor, 
                             extent=e[1] - e[0], start=e[0], style="pieslice", width=width)

def polygon(coords, outlineColor, fillColor=None, filled=1, width=1):
    c = []
    for coord in coords:
        c.extend([coord[0], coord[1]])
    if fillColor is None: fillColor = outlineColor
    if not filled: fillColor = ""
    return _canvas.create_polygon(c, outline=outlineColor, fill=fillColor, width=width)

def text(pos, color, contents, size=12, style="normal", anchor="nw"):
    return _canvas.create_text(pos[0], pos[1], fill=color, text=contents, 
                              font=("Courier", str(size), style), anchor=anchor)

def changeText(id, newText):
    _canvas.itemconfigure(id, text=newText)

def refresh():
    if _canvas: _canvas.update_idletasks()
    if _root_window: _root_window.update()

def remove_from_screen(id):
    if _canvas and id: _canvas.delete(id)

def end_graphics():
    global _root_window
    if _root_window:
        _root_window.destroy()
        _root_window = None