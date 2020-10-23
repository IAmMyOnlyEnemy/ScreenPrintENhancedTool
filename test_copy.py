#coding=utf-8

import win32clipboard  # http://sourceforge.net/projects/pywin32/
from time import sleep

def copy(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
def paste():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data

if __name__ == "__main__":
    sleep(5)
    text = "Testing the “clip—board”: 📋"
    try: text = text.decode('utf8')  # Python 2 needs decode to make a Unicode string.
    except AttributeError: pass
    #print("%r" % text.encode('utf8'))
    copy(text)
    data = paste()
    #print("%r" % data.encode('utf8'))
    #print("OK" if text == data else "FAIL")

    try: print(data)
    except UnicodeEncodeError as er:
        print(er)
        #print(data.encode('utf8'))