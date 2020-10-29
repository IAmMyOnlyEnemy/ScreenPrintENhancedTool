import win32clipboard
from io import BytesIO
from pynput import keyboard
from pynput import mouse

def key_press_sim(str_to_type):
    '''
        Implement a key pressing simulator using pynput
    '''
    my_keys = dict(
                    TAB = keyboard.Key.tab,
                    ENTER = keyboard.Key.enter,
                    CLEAR = keyboard.Key.pause,
                    SPACE = keyboard.Key.space,
                    DOWN = keyboard.Key.down,
                    UP = keyboard.Key.up,
                    RIGHT = keyboard.Key.right,
                    LEFT = keyboard.Key.left,
                    RCTRL = keyboard.Key.ctrl_r,
                    LCTRL = keyboard.Key.ctrl_l,
                    DELETE = keyboard.Key.delete,
                    BACKSPACE = keyboard.Key.backspace,
                    ESC = keyboard.Key.esc,
                    PF1 = keyboard.Key.f1,
                    PF2 = keyboard.Key.f2,
                    PF3 = keyboard.Key.f3,
                    PF4 = keyboard.Key.f4,
                    PF5 = keyboard.Key.f5,
                    PF6 = keyboard.Key.f6,
                    PF7 = keyboard.Key.f7,
                    PF8 = keyboard.Key.f8,
                    PF9 = keyboard.Key.f9,
                    PF10 = keyboard.Key.f10,
                    PF11 = keyboard.Key.f11,
                    PF12 = keyboard.Key.f12
                    )
    try:
        press_single_key(my_keys[str_to_type.upper()])
    except:
        copy_paste_text(str_to_type)
        press_two_keys(keyboard.Key.ctrl,"v")


def press_single_key(input_key):
    '''
        Press a single key
    '''
    mykeyboard = keyboard.Controller()
    mykeyboard.press(input_key)
    mykeyboard.release(input_key)

def press_two_keys(hold_key,press_key):
    mykeyboard = keyboard.Controller()
    with mykeyboard.pressed(hold_key):
        mykeyboard.press(press_key)
        mykeyboard.release(press_key)

def position_mouse(x_pos=0, y_pos=0, press_b1=False):
    '''
        Move the mouse to a given location on screen and press left click if needed
    '''
    mymouse = mouse.Controller()
    mymouse.position = (x_pos,y_pos)
    if press_b1:
        mymouse.press(mouse.Button.left)
        mymouse.release(mouse.Button.left)

def get_spin_vals(is_num = True):
    '''
        Create a list for spinbox values as follows:
            is_num = True  --> list of numbers from 1 to 25
            is_num = False --> list of letters from A to Z
    '''
    vals = []
    if not is_num:
        for i in range(65, 91):
            vals.append(chr(i))
    else:
        for i in range(1, 100):
            if i<10:
                vals.append("0" + str(i))
            else:
                vals.append(str(i))
    return vals

def copy_img_to_clip(img = None):
    '''
        Copy the print screen to ClipBoard
    '''
    output = BytesIO()
    img.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def copy_paste_text(my_text):
    '''
        Copy text to clipboard
    '''
    #my_text = my_text.decode('utf8')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(my_text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()