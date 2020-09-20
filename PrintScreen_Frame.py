import tkinter as tk                
from tkinter import filedialog
from PIL import ImageGrab
from os import path
from io import BytesIO
import win32clipboard
from import_settings import get_settings, fill_file_from_dict

global mycolour
mycolour = "snow3"
#mycolour = "#00ffff"

global global_settings
global_settings = get_settings()


class PrintScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=mycolour)
        self.controller = controller

        self.pathentry=MyEntry(parent=self, entry_setts=[51, 10, 8])
        self.imglabel=MyLabel(parent=self, label_setts=[25, "w", 10, 30])
        self.imglabel.config(justify=tk.LEFT)

        frmrdbt = tk.Frame(self,width=15, height=10)
        frmrdbt.place(x=240,y=55)
        self.tso_option=tk.StringVar()
        self.tso_option.set(global_settings['TSO_option'][0])
        self.reslabel=MyLabel(parent=self, label_setts=[18, "e", 245, 30])
        cics_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.tso_option,val="CICS")
        tso_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.tso_option,val="TSO")
        cics_radbutt.config(command=self.update_frame_res)
        tso_radbutt.config(command=self.update_frame_res)
        
        self.update_frame_res()
        self.statuslabel=MyLabel(parent=self, label_setts=[35, "w", 10, 200])
        self.statuslabel.set_label("Ready!")

        self.image_bbr = tk.PhotoImage(file="Images\\Browse_button.png")
        self.browse_button = tk.Button(self,
                            command=self.browse_command,
                            image=self.image_bbr,
                            text="Browse",
                            compound=tk.LEFT
                            ).place(x=322,y=3)
        self.image_bpic = tk.PhotoImage(file="Images\\Pic_button.png")
        self.print_button = tk.Button(self,
                            command=self.pic_cmd,
                            image=self.image_bpic,
                            text="PrintScreen",
                            compound=tk.TOP
                            ).place(x=297,y=90)
        self.up_button = tk.Button(self,
                            text="Up",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.move_up()),
                            width=3
                            ).place(x=10,y=170)
        self.down_button = tk.Button(self,
                            text="Dn",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.move_down()),
                            width=3
                            ).place(x=50,y=170)
        self.del_button = tk.Button(self,
                            text="Del",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.delete_item()),
                            width=4
                            ).place(x=170,y=170)

        frmlst = tk.Frame(self,width=15, height=50)
        frmlst.place(x=90,y=80)

        self.screenlist = MyList(parent=frmlst)
        self.screenlist.bind('<<ListboxSelect>>', self.onselect_listbox)

        num_vals = self.get_spin_vals(0)
        lett_vals = self.get_spin_vals(1)
        self.spin1 = MySpinbox(parent=self,spinvals=num_vals,pos_x=10)
        self.spin1.config(command=self.set_img_name)
        self.spin2 = MySpinbox(parent=self,spinvals=lett_vals,pos_x=50)
        self.spin2.config(command=self.set_img_name)
        self.spin3 = MySpinbox(parent=self,spinvals=num_vals,pos_x=190)
        self.spin3.config(command=self.set_img_name)

        self.checkbox1 = MyCheckbox(parent=self,pos_x=12)
        self.checkbox1.set_checkbox(global_settings['checkbox_options'][0])
        self.checkbox2 = MyCheckbox(parent=self,pos_x=52)
        self.checkbox2.set_checkbox(global_settings['checkbox_options'][1])
        self.checkbox3 = MyCheckbox(parent=self,pos_x=92)
        self.checkbox3.set_checkbox(global_settings['checkbox_options'][2])
        self.checkbox4 = MyCheckbox(parent=self,pos_x=192)
        self.checkbox4.set_checkbox(global_settings['checkbox_options'][3])
        
        self.ontopcheckbox = MyCheckbox(parent=self,pos_x=300)
        self.ontopcheckbox.config(text="Stay on top")
        self.ontopcheckbox.config(command=self.toggleontop)

        self.clipboardcheckbox = MyCheckbox(parent=self,pos_x=250)
        self.clipboardcheckbox.config(text="Copy")
        self.clipboardcheckbox.place(x=320,y=198)

        self.listentry=MyEntry(parent=self, entry_setts=[12, 90, 175])
        self.listentry.bind('<Return>', self.onenter_entry)
        
        self.set_img_name()

    def browse_command(self):
        folder_path = filedialog.askdirectory(
            title="Select where to save the images",
            initialdir=self.pathentry.get_entry()
            )
        if folder_path != "":
            self.pathentry.set_entry(folder_path)
        self.update_settings()

    def get_spin_vals(self,vals_type):
        vals = []
        if vals_type == 1:
            for i in range(65, 91):
                vals.append(chr(i))
        else:
            for i in range(1, 26):
                if i<10:
                    vals.append("0" + str(i))
                else:
                    vals.append(str(i))
        return vals

    def pic_cmd(self):
        try:
            img = ImageGrab.grab(bbox=self.img_frame())
            img.save(self.pathentry.get_entry() + '\\' + 
                     self.imglabel.get_label() + ".jpg", "jpeg")
            
            if self.checkbox1.get_checkbox():
                self.spin1.spinNext()
            if self.checkbox2.get_checkbox():
                self.spin2.spinNext()
            if self.checkbox3.get_checkbox():
                self.screenlist.set_next()
            if self.checkbox4.get_checkbox():
                self.spin3.spinNext()

            if self.clipboardcheckbox.get_checkbox():
                output = BytesIO()
                img.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

            self.statuslabel.set_label("Picture saved")
            self.set_img_name()
        except:
            self.statuslabel.set_label("Could not save picture")

    def img_frame(self):
        '''
        The frame for the print screen is a rectangle created by this values:
            * x position of upper-left corner
            * y position of upper-left corner
            * dimension in x direction
            * dimension in y direction
        This values can be modified in the settings.txt file
        '''

        x1 = global_settings[self.tso_option.get() + '_dimmension'][0]
        if x1 < 1:
            x1 = 1
        y1 = global_settings[self.tso_option.get() + '_dimmension'][1]
        if y1 < 1:
            y1 = 1
        x2 = x1 + global_settings[self.tso_option.get() + '_dimmension'][2]
        if x2 > self.winfo_screenwidth():
            x2 = self.winfo_screenwidth()
        y2 = y1 + global_settings[self.tso_option.get() + '_dimmension'][3]
        if y2 > self.winfo_screenheight():
            y2 = self.winfo_screenheight()
        frame = (x1, y1, x2, y2)
        return frame

    def get_img_name(self):
        return (self.spin1.get_spin() + 
                self.spin2.get_spin() + "_" +
                self.screenlist.get_selected() + "_" +
                self.spin3.get_spin()
                )

    def set_img_name(self):
        self.imglabel.set_label(self.get_img_name())
        self.imglabel.config(font=("Monospac821 BT",10))
        self.listentry.set_entry(self.screenlist.get_selected())
        if path.exists(self.pathentry.get_entry() + '\\' + 
                       self.imglabel.get_label()  + ".jpg"):
            self.imglabel.config(fg="Red")
        else:
            self.imglabel.config(fg="Black")

    def onselect_listbox(self, evt):
        self.set_img_name()

    def update_frame_res(self):
        self.reslabel.set_label(
                "{0} x {1} [{2}x{3}]".format(
                                    global_settings[self.tso_option.get() + '_dimmension'][2],
                                    global_settings[self.tso_option.get() + '_dimmension'][3],
                                    self.winfo_screenwidth(),
                                    self.winfo_screenheight())
                                )

    def onenter_entry(self,evt):
        self.screenlist.insert_new(self.listentry.get_entry())

    def toggleontop(self):
        if self.ontopcheckbox.get_checkbox():
            self.controller.wm_attributes("-topmost", 1)
            self.statuslabel.set_label("Always on top activated")
        else:
            self.controller.wm_attributes("-topmost", 0)
            self.statuslabel.set_label("Always on top deactivated")

    def update_settings(self):
        global_settings['TSO_option'][0] = self.tso_option.get()
        global_settings["checkbox_options"][0] = int(self.checkbox1.get_checkbox()==True)
        global_settings["checkbox_options"][1] = int(self.checkbox2.get_checkbox()==True)
        global_settings["checkbox_options"][2] = int(self.checkbox3.get_checkbox()==True)
        global_settings["checkbox_options"][3] = int(self.checkbox4.get_checkbox()==True)
        global_settings["screen_list"] = []
        for i, list_value in enumerate(self.screenlist.get(0, tk.END)):
            global_settings["screen_list"].append(list_value)
        global_settings['save_path'][0] = self.pathentry.get_entry()
        fill_file_from_dict("Settings\\settings.txt",global_settings)


class MyEntry(tk.Entry):
    def __init__(self,parent,entry_setts):
        self.entry_var = tk.StringVar()
        tk.Entry.__init__(self,parent,
                            #bg=mycolour,
                            justify=tk.LEFT,
                            textvariable=self.entry_var,
                            width=entry_setts[0]
                            )
        self.entry_var.set(global_settings['save_path'][0])
        self.place(x=entry_setts[1],y=entry_setts[2])

    def set_entry(self, new_text):
        self.entry_var.set(new_text)

    def get_entry(self):
        return self.entry_var.get()

class MyLabel(tk.Label):
    def __init__(self,parent,label_setts):
        tk.Label.__init__(self,
                            parent,
                            width=label_setts[0],
                            anchor=label_setts[1],
                            font=("Monospace",10),
                            bg=mycolour,
                            justify=tk.LEFT
                            )
        self.label_var = tk.StringVar()
        self.config(textvariable=self.label_var)
        self.place(x=label_setts[2],y=label_setts[3])

    def set_label(self, new_text):
        self.label_var.set(new_text)

    def get_label(self):
        return self.label_var.get()

class MyRadiobutt(tk.Radiobutton):
    def __init__(self,parent=None,op_val=None,val=""):
        tk.Radiobutton.__init__(self,
                                parent,
                                text=val,
                                value=val,
                                variable=op_val,
                                anchor="w",
                                width=4,
                                bg=mycolour,
                                indicatoron=0
                                )
        self.pack(fill=tk.BOTH)

class MyList(tk.Listbox):
    def __init__(self,parent):
        tk.Listbox.__init__(self,
                            parent,
                            exportselection=0,
                            font=("Monospace",10),
                            selectmode=tk.SINGLE,
                            height=5,
                            width=10
                            )
        
        for i, item in enumerate(global_settings["screen_list"]):
            self.insert(tk.END, item)

        self.listdim=len(global_settings["screen_list"])
        self.mylistscrollbar=tk.Scrollbar(parent, orient="vertical", width=20)
        self.mylistscrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.mylistscrollbar.config(command=self.yview)
        self.config(yscrollcommand=self.mylistscrollbar.set)
        self.select_set(0)
        self.pack(side=tk.LEFT)

    def get_selected(self):
        return self.get(self.curselection())

    def set_next(self):
        try:
            pos = self.curselection()[0] + 1
            if pos < self.listdim:
                self.selection_clear(0,tk.END)
                self.select_set(pos)
            else:
                pass
        except:
            pass

    def insert_new(self,newitem):
        itemnotexist = True
        for i, listitem in enumerate(self.get(0,tk.END)):
            if listitem == newitem:
                itemnotexist = False

        if itemnotexist:
            self.listdim =+ 1
            try:
                pos=self.curselection()[0]
                self.insert(pos+1, newitem)
            except:
                self.insert(tk.END, newitem)

    def move_up(self):
        try:
            pos=self.curselection()[0]
            text=self.get(pos)
            if pos != 0:
                self.delete(pos)
                self.insert(pos-1, text)
                self.select_set(pos-1)
                return "Item moved up"
            else:
                return "Cannot move item up"
        except:
            return "Impossible to move up"

    def move_down(self):
        try:
            pos=self.curselection()[0]
            text=self.get(pos)
            if pos != self.listdim - 1:
                self.delete(pos)
                self.insert(pos+1, text)
                self.select_set(pos+1)
                return "Item moved down"
            else:
                return "Cannot move item down"
        except:
            return "Impossible to move down"

    def delete_item(self):
        try:
            self.delete(self.curselection())
            self.listdim -= 1
            return "Item deleted"
        except:
            return "Delete not possible"

class MySpinbox(tk.Spinbox):
    def __init__(self,parent=None,spinvals=None,pos_x=0):
        self.spin_var = tk.StringVar()
        tk.Spinbox.__init__(self,
                            parent,
                            #bg=mycolour,
                            textvariable=self.spin_var,
                            values=spinvals,
                            width=3,
                            justify="center"
                            )
        self.place(x=pos_x,y=80)

    def spinNext(self):
        next_idx = self.spin_var.get()
        try:
            if self.spin_var.get() == "25":
                pass
            else:
                next_idx = str(int(self.spin_var.get()) + 1)
                if len(next_idx) == 1:
                    next_idx = "0" + next_idx
        except ValueError:
            try:
                if self.spin_var.get() == "Z":
                    pass
                else:
                    next_idx=chr(ord(self.spin_var.get()) + 1)
            except:
                pass
        self.spin_var.set(next_idx)

    def spinPrev(self):
        prev_idx = self.spin_var.get()
        try:
            if self.spin_var.get() == "01":
                pass
            else:
                prev_idx = str(int(self.spin_var.get()) - 1)
                if len(prev_idx) == 1:
                    prev_idx = "0" + prev_idx
        except ValueError:
            try:
                if self.spin_var.get() == "A":
                    pass
                else:
                    prev_idx=chr(ord(self.spin_var.get()) - 1)
            except:
                pass
        self.spin_var.set(prev_idx)

    def get_spin(self):
        return self.spin_var.get()

class MyCheckbox(tk.Checkbutton):
    def __init__(self,parent=None,pos_x=0):
        self.checkbox_var = tk.IntVar()
        tk.Checkbutton.__init__(self,
                                parent,
                                bg=mycolour,
                                variable=self.checkbox_var,
                                onvalue=1,
                                offvalue=0
                                )
        self.place(x=pos_x,y=53)

    def get_checkbox(self):
        if self.checkbox_var.get() == 1:
            return True
        else:
            return False

    def set_checkbox(self,myvar):
        self.checkbox_var.set(myvar)
