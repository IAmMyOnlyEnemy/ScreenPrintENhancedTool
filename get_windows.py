'''
https://www.blog.pythonlibrary.org/2014/10/20/pywin32-how-to-bring-a-window-to-front/
'''

from win32gui import EnumWindows, ShowWindow, GetWindowText, SetForegroundWindow




def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, GetWindowText(hwnd)))

if __name__ == "__main__":
    results = []
    top_windows = []
    EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if i[1] != '':
            print(i)
        '''
        if "notepad" in i[1].lower():
            print(i)
            ShowWindow(i[0],5)
            SetForegroundWindow(i[0])
            break
        '''