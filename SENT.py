import tkinter as tk                
from tkinter import ttk            
from PrintScreen_Frame import *

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Screen ENhanced Tool")

        self.minsize(width=400,height=250)
        self.maxsize(width=400,height=250)
        self.geometry("{0}x{1}".format(400, 250))
        
        self.wm_iconbitmap("Images\\STEN_icon.ico")

        container = ttk.Notebook(self)
        container.pack(side="top", fill="both", expand=True)

        PSFrame = PrintScreen(parent=container, controller=self)
        PSFrame.pic_cmd()

        CPFrame = ChainPrints(parent=container, controller=self)
        container.add(PSFrame,text="Print Screen")
        container.add(CPFrame,text="Chain Prints")

class ChainPrints(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1")#, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           #command=lambda: controller.show_frame("PrintScreen"))
                           command=self.aaaaa)
        button.pack(side="right", fill="x", pady=10)
        test_var = tk.StringVar()
        test_var.set("A-A-A-A-A-A")
        testlabel = tk.Entry(self,
                                bg="#00ffff",
                                justify=tk.LEFT,
                                textvariable=test_var,
                                width=25
                                )
        testlabel.pack(side="right", fill="x", pady=10)
        test_var_text = tk.StringVar()
        self.test_text = tk.Text(self,
                                #textvariable=self.test_var_text,
                                width=40,
                                height=5
                                )
        self.test_text.pack(side="left", fill="x", pady=10)
        #self.foyer_list = []

    def aaaaa(self):
        self.foyer_list = []
        line_list = self.test_text.get('1.0', 'end').split('\n')
        for line in line_list:
            if line != '':
                self.foyer_list.append(line)

        print(self.foyer_list)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()