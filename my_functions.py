import win32clipboard
from io import BytesIO
from pynput import keyboard
from pynput import mouse

def key_press_sim(str_to_type):
    '''
        Implement a key pressing simulator using pynput
    '''
    if str_to_type.upper() == "TAB":
        press_single_key(keyboard.Key.tab)
    elif str_to_type.upper() == "ENTER":
        press_single_key(keyboard.Key.enter)
    elif str_to_type.upper() == "PF1":
        press_single_key(keyboard.Key.f1)
    elif str_to_type.upper() == "PF2":
        press_single_key(keyboard.Key.f2)
    elif str_to_type.upper() == "PF3":
        press_single_key(keyboard.Key.f3)
    elif str_to_type.upper() == "PF4":
        press_single_key(keyboard.Key.f4)
    elif str_to_type.upper() == "PF5":
        press_single_key(keyboard.Key.f5)
    elif str_to_type.upper() == "PF6":
        press_single_key(keyboard.Key.f6)
    elif str_to_type.upper() == "PF7":
        press_single_key(keyboard.Key.f7)
    elif str_to_type.upper() == "PF8":
        press_single_key(keyboard.Key.f8)
    elif str_to_type.upper() == "PF9":
        press_single_key(keyboard.Key.f9)
    elif str_to_type.upper() == "PF10":
        press_single_key(keyboard.Key.f10)
    elif str_to_type.upper() == "PF11":
        press_single_key(keyboard.Key.f11)
    elif str_to_type.upper() == "PF12":
        press_single_key(keyboard.Key.f12)
    elif str_to_type.upper() == "CLEAR":
        press_single_key(keyboard.Key.pause)
    elif str_to_type.upper() == "SPACE":
        press_single_key(keyboard.Key.space)
    else:
        #for i in str_to_type:
        #    press_single_key(i)
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
        for i in range(1, 26):
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