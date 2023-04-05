# import all necessary modules
import speedtest  # pip install speedtest-cli
import datetime
from tkinter import Tk, PhotoImage, Label, Entry, StringVar, Button, Checkbutton, IntVar, Menu
import sys
import os


"""
** NetSpeed **
* A Python, simple internet speed meter.
* Do you ever find yourself bored with online speed meters and bad advertising?
* Then this is for you!
* Simple gui with Python, using speedtest-cli & Tkinter modules to test your internet connection.
* User can press "Test" :button or 'Alt + t' :keys for ease and convenience.
* Log supported 
"""


class Netspeed:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("NetSpeed")
        self.root.geometry('390x180')
        self.root.resizable(False, False)
        self.root.config(bg='#040404')
        self.bg = PhotoImage(file=self.resource_path("bg.png"))  # background image
        self.root.iconbitmap(self.resource_path("netspeed.ico"))

        # * variables *
        self.st = speedtest.Speedtest()
        self.st.get_servers()
        self.download = StringVar()  # download speed in Mbps
        self.upload = StringVar()  # upload speed in Mbps
        self.checkbox = IntVar()
        self.path = ''  # log path
        self.check_log()  # register log path

        # * labels, entries, buttons & checkbox *
        self.label = Label(self.root, image=self.bg)
        self.label.place(relx=0.5, rely=0.5, anchor='center')
        # *
        self.label2 = Label(self.root, bg='#040404')
        self.label2.pack(anchor='w', padx=4, pady=4)
        self.label3 = Label(self.label2, text="Download Speed: ", font='Arial 10 bold',
                            fg='#a6a6ff', bg='#040404')
        self.label3.pack(side='left', padx=4, pady=4)
        self.entry = Entry(self.label2, textvariable=self.download, font='Arial 10 bold', width=32, fg='black',
                           bg='#a6acf9', bd=2)
        self.entry.pack(side='left', padx=4, pady=4)
        # *
        self.label4 = Label(self.root, bg='#040404')
        self.label4.pack(anchor='w', padx=4, pady=4)
        self.label5 = Label(self.label4, text=f'Upload Speed:{"  "*3}', font='Arial 10 bold',
                            fg='#a6a6ff', bg='#040404')
        self.label5.pack(side='left', padx=4, pady=4)
        self.entry2 = Entry(self.label4, textvariable=self.upload, font='Arial 10 bold', width=32, fg='black',
                            bg='#a6acf9', bd=2)
        self.entry2.pack(side='left', padx=4, pady=4)
        # *
        self.button_test = Button(self.root, text="T\u0331est", font='Arial 10 bold', width=8, fg='orange',
                                  bg="#040404", activebackground='#125d9a', bd=2,
                                  command=lambda: [self.button_test.config(text="Wait!", fg='orange', relief='sunken',
                                                                           state='disabled', bg='#040404'),
                                                   self.button_test.after(100, self.speed_check)])
        self.button_test.pack(pady=16)
        self.buttonbox_log = Checkbutton(self.root, text="L\u0331og", font='Arial 8 bold', fg='orange', bg='#040404',
                                         selectcolor='#040404', activeforeground='orange', activebackground='#040404',
                                         variable=self.checkbox, onvalue=1, offvalue=0, command=self.checkbox_state)
        self.buttonbox_log.pack(anchor='w', padx=4)

        # * buttons dictionary *
        self.buttons_ = {
                        "t": (self.button_test, self.speed_check)
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: [self.pressed(event.char), self.buttons_[event.char][1]()])
        # *
        self.root.bind('<Alt-l>', lambda event: [self.checkbox.set(0) if self.checkbox.get() else self.checkbox.set(1),
                                                 self.checkbox_state()])

        # * mouse menu *
        self.entry.bind("<Button-3>", self.mouse_menu)
        self.entry2.bind("<Button-3>", self.mouse_menu)

    # *** Methods ***

    def check_log(self):
        # ** check for logging file **
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = "netspeed.txt"
        self.path = os.path.join(path, file)
        # print(self.path)  # test
        try:  # check previous checkbox state
            with open(self.path, 'r') as f:
                line1 = f.readline()
                if line1 == "1\n":
                    self.checkbox.set(1)
        except FileNotFoundError:
            pass

    def checkbox_state(self):
        # ** check box option state **
        ticked = self.checkbox.get()
        if ticked:
            data = ''
            check = False
            try:  # check for logging file
                with open(self.path, 'r') as f:
                    data = f.read()
                    if data[0:2] != "1\n":
                        check = True
            except FileNotFoundError:
                check = True
            if check:  # create & activate log
                with open(self.path, 'w') as f:
                    f.write("1\n" + data)
        else:  # not ticked
            data = ''
            check = False
            try:   # check for active log
                with open(self.path, 'r') as f:
                    data = f.read()
                    if data[0:2] == "1\n":
                        check = True
            except FileNotFoundError:
                pass
            if check:  # deactivate log
                with open(self.path, 'w') as f:
                    modified = data[2:]
                    f.write(modified)

    def speed_check(self):
        # ** check internet download & upload speed **
        down = str(round(self.st.download()/10**6, 3)) + " Mbps"
        self.download.set(down)
        up = str(round(self.st.upload()/10**6, 3)) + " Mbps"
        self.upload.set(up)
        self.button_test.config(text="T\u0331est", relief='raised', state='normal', bg='#040404')
        ticked = self.checkbox.get()
        if ticked:
            self.create_log()

    def create_log(self):
        # ** create log with timestamps **
        timestamp = datetime.datetime.now()
        download = self.download.get()
        upload = self.upload.get()
        log = f'{download} / {upload} - {timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n'
        with open(self.path, 'a') as f:
            f.write(log)

    def pressed(self, letter):
        # ** shortcut effect **
        self.buttons_[letter][0].config(relief='sunken', state='disabled')
        self.buttons_[letter][0].after(150, lambda: self.buttons_[letter][0].config(relief='raised', state='normal'))

    @staticmethod
    def mouse_menu(event):
        # ** right click menu **
        mouse_menu = Menu(None, tearoff=0, takefocus=0)
        # * menu options *
        for option in ["Cut", "Copy", "Paste"]:
            mouse_menu.add_command(label=option, command=lambda cmd=option: event.widget.event_generate(f'<<{cmd}>>'))
        mouse_menu.tk_popup(event.x_root, event.y_root, entry='0')

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** keep window visible **
        self.root.mainloop()


def main():
    speed_meter = Netspeed()
    speed_meter.run()  # keep NetSpeed window 'alive'


if __name__ == '__main__':
    main()  # executed only from netspeed.py
