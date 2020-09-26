import win32clipboard
from io import BytesIO
from pynput.keyboard import Key, Controller as Key_Control
from pynput.mouse import Button, Controller as Ms_Controller

def key_press_sim(str_to_type):
    '''
        Implement a key pressing simulator using pynput
    '''
    keyboard = Key_Control()
    if str_to_type.upper() == "TAB":
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif str_to_type.upper() == "ENTER":
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif str_to_type.upper() == "PF1":
        keyboard.press(Key.f1)
        keyboard.release(Key.f1)
    elif str_to_type.upper() == "PF2":
        keyboard.press(Key.f2)
        keyboard.release(Key.f2)
    elif str_to_type.upper() == "PF3":
        keyboard.press(Key.f3)
        keyboard.release(Key.f3)
    elif str_to_type.upper() == "PF4":
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
    elif str_to_type.upper() == "PF5":
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif str_to_type.upper() == "PF6":
        keyboard.press(Key.f6)
        keyboard.release(Key.f6)
    elif str_to_type.upper() == "PF7":
        keyboard.press(Key.f7)
        keyboard.release(Key.f7)
    elif str_to_type.upper() == "PF8":
        keyboard.press(Key.f8)
        keyboard.release(Key.f8)
    elif str_to_type.upper() == "PF9":
        keyboard.press(Key.f9)
        keyboard.release(Key.f9)
    elif str_to_type.upper() == "PF10":
        keyboard.press(Key.f10)
        keyboard.release(Key.f10)
    elif str_to_type.upper() == "PF10":
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)
    elif str_to_type.upper() == "PF12":
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
    else:
        keyboard.type(str_to_type)

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