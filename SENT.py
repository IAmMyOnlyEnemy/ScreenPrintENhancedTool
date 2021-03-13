import tkinter as tk                
from tkinter import ttk            
from tkinter import filedialog
from PIL import ImageGrab
from os import path
from time import sleep
from import_settings import get_settings, fill_file_from_dict
from my_functions import key_press_sim, get_spin_vals, copy_img_to_clip
from win32gui import EnumWindows, ShowWindow, GetWindowText, SetForegroundWindow

global global_settings
global_settings = get_settings()

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Screen ENhanced Tool")

        self.minsize(width=400,height=305)
        self.maxsize(width=400,height=305)
        self.geometry("{0}x{1}".format(400, 305))
        
        try:
            self.wm_iconbitmap("Images\\STEN_icon.ico")
        except:
            pass

        container = ttk.Notebook(self)
        container.pack(side="top", fill="both", expand=True)

        PSFrame = PrintScreen(parent=container, controller=self)
        CPFrame = ChainPrints(parent=container, controller=self)
        STFrame = SettingTab(parent=container, controller=self)

        container.add(PSFrame,text="Print Screen")
        container.add(CPFrame,text="Chain Prints")
        container.add(STFrame,text="Settings")

class PrintScreen(tk.Frame):
    '''
        This frame is for manually saving images according to my desire
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg=global_settings['app_colour'])
        self.controller = controller

        self.pathentry=MyEntry(parent=self, entry_setts=[51, 10, 8])
        self.imglabel=MyLabel(parent=self, label_setts=[25, "w", 10, 30])
        self.imglabel.config(justify=tk.LEFT)

        self.reslabel=MyLabel(parent=self, label_setts=[18, "e", 245, 30])

        try:
            self.image_bbr = tk.PhotoImage(file="Images\\Browse_button.png")
        except:
            self.image_bbr = None

        self.browse_button = tk.Button(self,
                            command=self.browse_command,
                            image=self.image_bbr,
                            text="Browse",
                            background=global_settings['app_colour'],
                            activebackground="DarkSeaGreen2",
                            compound=tk.LEFT
                            ).place(x=322,y=3)

        self.checkbox1 = MyCheckbox(parent=self,pos_x=12)
        self.checkbox1.set_checkbox(global_settings['checkbox_options'][0])
        self.checkbox2 = MyCheckbox(parent=self,pos_x=52)
        self.checkbox2.set_checkbox(global_settings['checkbox_options'][1])
        self.checkbox3 = MyCheckbox(parent=self,pos_x=92)
        self.checkbox3.set_checkbox(global_settings['checkbox_options'][2])
        self.checkbox4 = MyCheckbox(parent=self,pos_x=192)
        self.checkbox4.set_checkbox(global_settings['checkbox_options'][3])
        
        frmrdbt = tk.Frame(self,width=15, height=10)
        frmrdbt.place(x=240,y=55)
        self.screen_option=tk.StringVar()
        self.screen_option.set(global_settings['screen_option'][0])
        
        opt1_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt1")
        opt2_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt2")
        opt3_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt3")
        opt1_radbutt.config(command=self.update_frame_res)
        opt2_radbutt.config(command=self.update_frame_res)
        opt3_radbutt.config(command=self.update_frame_res)
        self.update_frame_res()

        self.ontopcheckbox = MyCheckbox(parent=self,pos_x=300)
        self.ontopcheckbox.config(text="Stay on top")
        self.ontopcheckbox.config(command=self.toggleontop)
        
        num_vals = get_spin_vals()
        lett_vals = get_spin_vals(is_num=False)
        self.spin1 = MySpinbox(parent=self,spinvals=num_vals,pos_x=10)
        self.spin1.config(command=self.set_img_name)
        self.spin2 = MySpinbox(parent=self,spinvals=lett_vals,pos_x=50)
        self.spin2.config(command=self.set_img_name)

        frmlst = tk.Frame(self,width=15, height=50)
        frmlst.place(x=90,y=80)
        self.screenlist = MyList(parent=frmlst)
        self.screenlist.bind('<<ListboxSelect>>', self.onselect_listbox)

        self.spin3 = MySpinbox(parent=self,spinvals=num_vals,pos_x=190)
        self.spin3.config(command=self.set_img_name)
        
        self.statuslabel=MyLabel(parent=self, label_setts=[35, "w", 10, 255])
        self.statuslabel.set_label("Ready!")

        try:
            self.image_bpic = tk.PhotoImage(file="Images\\Pic_button.png")
        except:
            self.image_bpic = None
            
        self.print_button = tk.Button(self,
                            command=self.pic_cmd,
                            image=self.image_bpic,
                            text="PrintScreen",
                            background=global_settings['app_colour'],
                            activebackground="DarkSeaGreen2",
                            compound=tk.TOP
                            ).place(x=297,y=90)

        self.up_button = tk.Button(self,
                            text="Up",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.move_up()),
                            background=global_settings['app_colour'],
                            activebackground="DarkSeaGreen2",
                            width=9
                            ).place(x=10,y=110)

        self.down_button = tk.Button(self,
                            text="Down",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.move_down()),
                            background=global_settings['app_colour'],
                            activebackground="DarkSeaGreen2",
                            width=9
                            ).place(x=10,y=140)

        self.listentry=MyEntry(parent=self, entry_setts=[12, 10, 180])
        self.listentry.bind('<Return>', self.onenter_entry)

        self.del_button = tk.Button(self,
                            text="Delete",
                            compound="center",
                            command=lambda: self.statuslabel.set_label(self.screenlist.delete_item()),
                            background=global_settings['app_colour'],
                            activebackground="tomato",
                            width=9
                            ).place(x=10,y=210)
        
        self.clipboardcheckbox = MyCheckbox(parent=self,pos_x=250)
        self.clipboardcheckbox.config(text="Copy")
        self.clipboardcheckbox.place(x=320,y=198)

        self.set_img_name()

    def browse_command(self):
        '''
            Get the folder adress where the pictures will be saved
        '''
        folder_path = filedialog.askdirectory(
            title="Select where to save the images",
            initialdir=self.pathentry.get_entry()
            )
        if folder_path != "":
            self.pathentry.set_entry(folder_path)
            global_settings['save_path'][0] = folder_path
        self.update_settings()

    def pic_cmd(self):
        '''
            Save the print screen as jpg
        '''
        try:
            take_printscreen(frame_op = self.screen_option.get(),
                            screen_w = self.winfo_screenwidth(), 
                            screen_h = self.winfo_screenheight(), 
                            image_name = self.imglabel.get_label(), 
                            copy_to_clip = self.clipboardcheckbox.get_checkbox())
            if self.checkbox1.get_checkbox():
                self.spin1.spinNext()
            if self.checkbox2.get_checkbox():
                self.spin2.spinNext()
            if self.checkbox3.get_checkbox():
                self.screenlist.set_next()
            if self.checkbox4.get_checkbox():
                self.spin3.spinNext()

            self.statuslabel.set_label("Picture saved")
            self.set_img_name()
        except:
            self.statuslabel.set_label("Could not save picture")

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

    def update_frame_res(self):
        self.reslabel.set_label(
                "{0} x {1} [{2}x{3}]".format(
                                    global_settings[self.screen_option.get() + '_dimmension'][2],
                                    global_settings[self.screen_option.get() + '_dimmension'][3],
                                    self.winfo_screenwidth(),
                                    self.winfo_screenheight()
                                    )
                                )

    def onselect_listbox(self, evt):
        self.set_img_name()

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
        global_settings['screen_option'][0] = self.screen_option.get()
        global_settings["checkbox_options"][0] = int(self.checkbox1.get_checkbox()==True)
        global_settings["checkbox_options"][1] = int(self.checkbox2.get_checkbox()==True)
        global_settings["checkbox_options"][2] = int(self.checkbox3.get_checkbox()==True)
        global_settings["checkbox_options"][3] = int(self.checkbox4.get_checkbox()==True)
        global_settings["screen_list"] = []
        for i, list_value in enumerate(self.screenlist.get(0, tk.END)):
            global_settings["screen_list"].append(list_value)
        fill_file_from_dict("settings.txt",global_settings)

class ChainPrints(tk.Frame):
    '''
        This frame is for automatically saving images for a given list
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg=global_settings['app_colour'])
        self.controller = controller

        button = tk.Button(self,
                            text="Run",
                            width=8,
                            background="green2",
                            activebackground="OrangeRed2",
                            command=self.bt_action
                            )
        button.place(x=331,y=251)

        self.my_options = global_settings['my_screens']

        frmfoy = tk.Frame(self)
        frmfoy.place(x=5,y=5)
        self.foy_text = MyText(parent=frmfoy)

        frmaction = tk.Frame(self)
        frmaction.place(x=130,y=5)
        self.action_text = MyText(parent=frmaction)

        self.progdropbox = MyDropBox(parent=self)
        self.progdropbox.config(bg="alice blue")
        self.progdropbox["menu"].config(bg="alice blue")

        num_vals = get_spin_vals()
        lett_vals = get_spin_vals(is_num=False)
        self.delayspin = MySpinbox(parent=self,spinvals=num_vals,pos_x=250)
        self.delayspin.place(y=45)
        self.delaylabel = MyLabel(parent=self, label_setts=[17, "w", 282, 45])
        self.delaylabel.set_label("seconds to delay")
        self.spin1 = MySpinbox(parent=self,spinvals=num_vals,pos_x=250)
        self.spin2 = MySpinbox(parent=self,spinvals=lett_vals,pos_x=290)
        self.spin3 = MySpinbox(parent=self,spinvals=num_vals,pos_x=330)

        self.statuslabel = MyLabel(parent=self, label_setts=[40, "w", 5, 255])
        self.statuslabel.set_label("Ready!")

        self.print_name = ""

    def bt_action(self):
        '''
            This is the command attached to button "Run"
            It starts the process
        '''
        self.goto_sleep()
        self.foyer_list = self.foy_text.get_list()
        self.action_list = self.action_text.get_list()

        for self.foyer in self.foyer_list:
            self.print_name = ""
            for self.act in self.action_list:
                self.goto_sleep()
                self.progdropbox.bring_to_front()
                self.action_time()
            self.spin2.spinNext()
                
    def goto_sleep(self):
        '''
            Pause the processing
        '''
        try:
            sleep(int(self.delayspin.get_spin()))
        except ValueError:
            sleep(10)

    def action_time(self):
        '''
            Evaluate the type of action to be performed:
        '''
        if self.act in global_settings['my_screens']:
            if self.act == "CONT":
                key_press_sim("{0} {1}".format(self.act,self.foyer))
            elif self.act[0] == 'Z':
                key_press_sim("PF9")
            else:
                key_press_sim(self.act)
            self.print_name = "{0}{1}_{2}_{3}".format(
                                        self.spin1.get_spin(),
                                        self.spin2.get_spin(),
                                        self.act,
                                        self.spin3.get_spin()
                                        )
        elif self.act[:4].upper() == 'DOWN':
            try:
                for i in range(0, int(self.act[5:].strip())):
                    key_press_sim("DOWN")
            except:
                pass
        elif self.act[:2].upper() == 'UP':
            try:
                for i in range(0, int(self.act[3:].strip())):
                    key_press_sim("UP")
            except:
                pass
        elif self.act[:5].upper() == 'RIGHT':
            try:
                for i in range(0, int(self.act[6:].strip())):
                    key_press_sim("RIGHT")
            except:
                pass
        elif self.act[:4].upper() == 'LEFT':
            try:
                for i in range(0, int(self.act[5:].strip())):
                    key_press_sim("LEFT")
            except:
                pass
        elif self.act.upper() == "PIC":
            try:
                take_printscreen(
                                frame_op = "opt1",
                                screen_w = self.winfo_screenwidth(), 
                                screen_h = self.winfo_screenheight(),
                                image_name = self.print_name,
                                copy_to_clip = False
                                )
                self.statuslabel.set_label("{} saved".format(self.print_name))
            except:
                self.statuslabel.set_label("Could not save image")
        else:
            self.goto_sleep()
            key_press_sim("{0}".format(self.act))
        self.statuslabel.set_label("Case {0}, operation {1}".format(self.foyer,self.act))

class SettingTab(tk.Frame):
    '''
        This frame is for manually saving images according to my desire
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg=global_settings['app_colour'])
        self.controller = controller

        frm_input = tk.Frame(self,
                            width=200,
                            height=50,
                            bg=global_settings['app_colour']
                            )
        frm_input.place(x=10,y=10)

        self.x1label=MyLabel(parent=frm_input, label_setts=[3, "w", 0, 0])
        self.x1label.set_label("x1:")
        self.y1label=MyLabel(parent=frm_input, label_setts=[3, "w", 0, 25])
        self.y1label.set_label("y1:")

        self.x1label=MyLabel(parent=frm_input, label_setts=[8, "w", 63, 0])
        self.x1label.set_label("x width:")
        self.y1label=MyLabel(parent=frm_input, label_setts=[8, "w", 63, 25])
        self.y1label.set_label("y width:")

        self.x1entry=MyEntry(parent=frm_input, entry_setts=[4,25,1])
        self.x1entry.set_entry("1234")
        self.y1entry=MyEntry(parent=frm_input, entry_setts=[4,25,26])
        self.y1entry.set_entry("2345")

        self.xwentry=MyEntry(parent=frm_input, entry_setts=[4,115,1])
        self.xwentry.set_entry("1100")
        self.ywentry=MyEntry(parent=frm_input, entry_setts=[4,115,26])
        self.ywentry.set_entry("1200")

        frm_dim_list = tk.Frame(self,width=20, height=50)
        frm_dim_list.place(x=90,y=80)
        self.frames_dim_list = MyList(parent=frm_dim_list)
        self.frames_dim_list.width = 20
        
        self.up_button = tk.Button(self,
                            text="Save",
                            compound="center",
                            #command=lambda: self.statuslabel.set_label(self.screenlist.move_up()),
                            background=global_settings['app_colour'],
                            activebackground="DarkSeaGreen2",
                            width=9
                            ).place(x=10,y=207)
        frmrdbt = tk.Frame(self,width=15, height=10)
        frmrdbt.place(x=10,y=80)
        self.screen_option=tk.StringVar()
        self.screen_option.set(global_settings['screen_option'][0])
        
        opt1_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt1")
        opt2_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt2")
        opt3_radbutt = MyRadiobutt(parent=frmrdbt,op_val=self.screen_option,val="opt3")
        #opt1_radbutt.config(command=self.update_frame_res)
        #opt2_radbutt.config(command=self.update_frame_res)
        #opt3_radbutt.config(command=self.update_frame_res)

class MyEntry(tk.Entry):
    def __init__(self,parent,entry_setts):
        self.entry_var = tk.StringVar()
        tk.Entry.__init__(self,parent,
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
                            bg=global_settings['app_colour'],
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
                                anchor="n",
                                width=4,
                                background=global_settings['app_colour'],
                                activebackground=global_settings['app_colour'],
                                selectcolor="spring green",
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
                            height=10,
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
            print("pos = {0}, listdim = {1}".format(pos,self.listdim))
            if pos < self.listdim:
                self.selection_clear(0,tk.END)
                self.select_set(pos)
            else:
                pass
        except:
            print("set next not possible")
            pass

    def insert_new(self,newitem):
        itemnotexist = True
        for i, listitem in enumerate(self.get(0,tk.END)):
            if listitem == newitem:
                itemnotexist = False
                break

        if itemnotexist:
            self.listdim += 1
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
                            textvariable=self.spin_var,
                            values=spinvals,
                            width=3,
                            justify="center"
                            )
        self.place(x=pos_x,y=80)

    def spinNext(self):
        next_idx = self.spin_var.get()
        try:
            if self.spin_var.get() == "99":
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
        try:
            return self.spin_var.get()
        except:
            pass

class MyCheckbox(tk.Checkbutton):
    def __init__(self,parent=None,pos_x=0):
        self.checkbox_var = tk.IntVar()
        tk.Checkbutton.__init__(self,
                                parent,
                                bg=global_settings['app_colour'],
                                activebackground=global_settings['app_colour'],
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

class MyText(tk.Text):
    def __init__(self,parent):
        tk.Text.__init__(self,
                        parent,
                        width=12,
                        height=15
                        )
        scrollb = tk.Scrollbar(parent,
                                orient="vertical",
                                command=self.yview)
        self['yscrollcommand'] = scrollb.set
        scrollb.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.pack(side=tk.LEFT,expand=True, fill='both')

    def get_list(self):
        txtlist = []
        line_list = self.get('1.0', 'end').split('\n')
        for line in line_list:
            if line.strip() != '':
                txtlist.append(line.strip().upper())
        return txtlist

class MyComboBox(ttk.Combobox):
    def __init__(self,parent,bg="red"):
        progs = []
        top_windows = []
        EnumWindows(self.windowEnumerationHandler, top_windows)
        for i in top_windows:
            if i[1] != '':
                progs.append(i[1])
        ttk.Combobox.__init__(self,
                            parent,
                            width=20,
                            value=progs
                            )
        self.current(0)
        self.place(x=250,y=5)

    def windowEnumerationHandler(self,hwnd,top_windows):
        top_windows.append((hwnd, GetWindowText(hwnd)))

class MyDropBox(tk.OptionMenu):
    def __init__(self,parent,bg="red"):
        progs = []
        top_windows = []
        EnumWindows(self.windowEnumerationHandler, top_windows)
        except_list = ['',
                        'Default IME',
                        'MSCTFIME UI',
                        'Window',
                        'Settings'
                        ]
        for i in top_windows:
            if i[1] not in except_list:
                progs.append([i[0],i[1]])
        progs.sort()
        self.myvar = tk.StringVar()
        self.myvar.set("{0}, {1}".format(global_settings['active_window'][0],global_settings['active_window'][1]))
        tk.OptionMenu.__init__(self,
                                parent,
                                self.myvar,
                                *progs,
                                )
        self.config(width=17)
        self.myvar.trace('w', self.get_dropdown)
        self.place(x=250,y=2)

    def windowEnumerationHandler(self,hwnd,top_windows):
        top_windows.append((hwnd, GetWindowText(hwnd)))

    def get_dropdown(self,*args):
        global_settings['active_window'][0] = int(self.myvar.get()[1:].split(", ")[0])
        global_settings['active_window'][1] = self.myvar.get().split(", ")[1][:-1]

    def bring_to_front(self):
        try:
            ShowWindow(global_settings['active_window'][0],5)
            SetForegroundWindow(global_settings['active_window'][0])
        except:
            pass

def take_printscreen(frame_op, screen_w, screen_h, image_name, copy_to_clip):
    '''
        The frame for the print screen is a rectangle created by this values:
            * x1 = x position of upper-left corner
            * y1 = y position of upper-left corner
            * x2 = dimension in x direction
            * y2 = dimension in y direction
        This values can be modified in the settings.txt file
    '''
    x1 = global_settings[frame_op + '_dimmension'][0]
    if x1 < 1:
        x1 = 1

    y1 = global_settings[frame_op + '_dimmension'][1]
    if y1 < 1:
        y1 = 1

    x2 = x1 + global_settings[frame_op + '_dimmension'][2]
    if x2 > screen_w:
        x2 = screen_w

    y2 = y1 + global_settings[frame_op + '_dimmension'][3]
    if y2 > screen_h:
        y2 = screen_h

    '''
       Take the printscreen using PIL.ImageGrab 
    '''
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img.save(global_settings['save_path'][0] + '\\' + image_name + ".jpg", "jpeg")

    '''
        Copy image to clipboard if option is on
    '''
    if copy_to_clip:
        copy_img_to_clip(img)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()