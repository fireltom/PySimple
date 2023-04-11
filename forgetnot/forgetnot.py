# import all necessary modules
from tkinter import Tk, PhotoImage, Canvas, Text, Entry, StringVar, Button, Menu
from plyer import notification
from infi.systray import SysTrayIcon
from infi.systray import win32_adapter
import sys
import os
import json

"""
** Forget Not **
* A Python simple notification reminder.
* Balloon tray reminder that will help you not to miss any plans, tasks and events from your daily life.
* Simple gui with Python, using plyer, infi.systray & Tkinter modules.
* User can press "Activate" / "Deactivate" :button or 'Alt + a' :key for ease and convenience.
"""


class ForgetNot:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("Forget Not")
        self.root.geometry('350x351')
        self.root.resizable(False, False)
        self.root.config(bg='#136799')
        self.bg = PhotoImage(file=self.resource_path("forgetnotbg.png"))  # background image
        self.ico = self.resource_path("forgetnot.ico")
        self.root.iconbitmap(self.ico)
        self.root.protocol('WM_DELETE_WINDOW', self.hide_root)

        # * variables *
        self.title = StringVar()
        self.title.trace_add('write', self.title_input)
        self.hour = StringVar()
        self.hour.trace_add('write', self.hour_input)
        self.minutes = StringVar()
        self.minutes.trace_add('write', self.minutes_input)
        self.clock = 0
        self.clockHour = 0
        self.clockMinutes = 0
        self.counter = 86341  # sec, guard value (23h + 59m + 1 sec)
        self.jsonCheck = True
        self.trayActivate = (("Show Window", None, self.show_root), ("Activate", None, self.tray_option))  # tray
        self.trayDeactivate = (("Show Window", None, self.show_root), ("Deactivate", None, self.tray_option))  # options

        # * canvas, entries, text, button & tray *
        self.canvas_bg = Canvas(self.root, bg='black')
        self.canvas_bg.pack()
        self.canvas_bg.create_image(0, 0, anchor='nw', image=self.bg)
        # *
        self.canvas_bg.create_text(25, 25, text="Title:", fill='#a6a6ff', font='Arial 13 bold')
        self.entry_title = Entry(self.canvas_bg, textvariable=self.title, font='Arial 12 bold', width=36, fg='black',
                                 bg='#a6acf9', bd=2)
        self.entry_title.pack(anchor='w', padx=8, pady=40)
        # *
        self.canvas_bg.create_text(34, 90, text="Notes:", fill='#a6a6ff', font='Arial 13 bold')
        self.text_notes = Text(self.canvas_bg, font='Arial 12 bold', width=36, height=7,
                               fg='#a6acf9', bg='#121212', relief='groove', wrap='word', bd=2)
        self.text_notes.pack(padx=8)
        self.text_notes.bind('<KeyRelease>', lambda event: self.notes_input())  # 'smart' text, limit 256 characters
        #  *
        self.canvas_bg.create_text(87, 265, text="Set Hour & Minutes:", fill='#a6a6ff', font='Arial 13 bold')
        self.entry_hour = Entry(self.canvas_bg, textvariable=self.hour, font='Arial 12 bold', width=2, fg='black',
                                bg='#a6acf9', bd=2)
        self.entry_hour.pack(side='left', anchor='w', padx=8, pady=40)
        self.canvas_bg.create_text(40, 295, text=":", fill='#a6a6ff', font='Arial 13 bold')
        self.entry_minutes = Entry(self.canvas_bg, textvariable=self.minutes, font='Arial 12 bold', width=2, fg='black',
                                   bg='#a6acf9', bd=2)
        self.entry_minutes.pack(side='left', anchor='w', padx=8, pady=40)
        # *
        self.button_activate = Button(self.canvas_bg, text="A\u0331ctivate", font='Arial 10 bold', width=9, fg='orange',
                                      bg="#040404", activebackground='#125d9a', bd=2,
                                      command=lambda: [[self.button_activate.config(text="Dea\u0331ctivate", fg='red'),
                                                        self.systray.update(menu_options=self.trayDeactivate),
                                                        self.button_activate.after(150, self.balloon_note)]
                                                       if self.button_activate['fg'] == 'orange'
                                                       else [self.button_activate.config(text="A\u0331ctivate",
                                                             fg='orange'),
                                                             self.systray.update(menu_options=self.trayActivate)]]
                                      )  # lambda, rollover: Activate <--> Deactivate

        self.button_activate.pack(side='bottom', anchor='e', padx=16, pady=16)
        # *
        self.systray = SysTrayIcon(self.ico, "ForgetNot", self.trayActivate, on_quit=self.quit_root)
        # *
        self.read_notification()  # check user previous inputs

        # * buttons dictionary *
        self.buttons_ = {
                        "a": [self.button_activate, self.button_state, "A\u0331activate", "Dea\u0331ctivate"],
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: [self.pressed(event.char), self.buttons_[event.char][1]()])

        # * mouse menu *
        self.entry_title.bind('<Button-3>', self.mouse_menu)
        self.text_notes.bind('<Button-3>', self.mouse_menu)
        self.entry_hour.bind('<Button-3>', self.mouse_menu)
        self.entry_minutes.bind('<Button-3>', self.mouse_menu)

    # *** Methods ***

    def title_input(self, var=None, index=None, mode=None, ret=None):
        # ** title length  **
        title = self.title.get()
        if len(title) > 64:
            self.title.set(title[:64])
        if ret and len(title):
            return True

    def notes_input(self, var=None, index=None, mode=None, ret=None):
        # ** text length  **
        text = self.text_notes.get(1.0, 'end-1c')
        if len(text) > 255:
            self.text_notes.delete(1.0, 'end')
            self.text_notes.insert(1.0, text[:255])
        if ret and text:
            return True

    def hour_input(self, var=None, index=None, mode=None, ret=None):
        # ** check hour input  **
        hour = self.hour.get()
        if hour.isdigit():
            if int(hour) > 23:
                self.hour.set("23")
            if ret:
                return True
        else:
            self.hour.set('')

    def minutes_input(self, var=None, index=None, mode=None, ret=None):
        # ** check minutes input  **
        minutes = self.minutes.get()
        if minutes.isdigit():
            if int(minutes) > 59:
                self.minutes.set("59")
            if ret:
                return True
        else:
            self.minutes.set('')

    def button_state(self):
        # ** check button state  **
        if self.button_activate['fg'] == 'red':
            self.button_activate.after(150, self.balloon_note)
        else:
            pass

    def balloon_note(self):
        # ** start notification 'reminder' **
        check = True
        if self.title_input(ret=check) and self.notes_input(ret=check) and self.hour_input(ret=check)\
           and self.minutes_input(ret=check):  # check integrity from all entries
            hour = int(self.hour.get())
            minutes = int(self.minutes.get())
            if not self.clock:
                if not hour + minutes:
                    minutes = 1
                self.hour.set(str(hour).zfill(2))
                self.minutes.set(str(minutes).zfill(2))
                self.clock = 60 * 60 * hour + 60 * minutes
                self.clockHour = hour
                self.clockMinutes = minutes
                self.counter = 0
                self.update_notification()  # update json
            if self.button_activate['fg'] == 'orange'\
               or self.clockHour != hour or self.clockMinutes != minutes:  # check for button or time changes & stop
                self.clock = 0
                self.counter = 86341
                self.button_activate.config(text="A\u0331ctivate", fg='orange')
            if self.clock == self.counter:
                self.counter = 0
                notification.notify(title=self.entry_title.get(), message=self.text_notes.get(1.0, 'end-1c'),
                                    app_name=self.root.title(), timeout=10,
                                    app_icon=self.resource_path("forgetnot.ico"))  # on Windows, app_icon has to be .ico
            if self.clock:
                self.counter += 60
                return self.root.after(60*1000, self.balloon_note)
        else:
            self.pressed("a")  # empty hour / minutes entry

    def read_notification(self):
        # ** check for json settings **
        directory = os.path.dirname(os.path.abspath(sys.argv[0]))  # app dir
        file = "forgetnot.json"
        path = os.path.join(directory, file)
        if self.jsonCheck:
            try:
                with open(path, 'r') as f:
                    dict_notification = json.load(f)
                self.title.set(dict_notification['title'][:64])
                self.text_notes.delete(1.0, 'end')
                self.text_notes.insert(1.0, dict_notification['notes'][:255])
                self.hour.set(dict_notification['hour'])
                self.minutes.set(dict_notification['minutes'])
            except Exception:
                pass
        self.jsonCheck = False

    def update_notification(self):
        # ** update json settings **
        dict_notification = {}
        directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        file = "forgetnot.json"
        path = os.path.join(directory, file)
        dict_notification['title'] = self.title.get()
        dict_notification['notes'] = self.text_notes.get(1.0, 'end-1c')
        dict_notification['hour'] = self.hour.get()
        dict_notification['minutes'] = self.minutes.get()
        with open(path, 'w') as f:
            json.dump(dict_notification, f)

    def quit_root(self, systray):
        # ** quit window **
        win32_adapter.DestroyWindow(systray._hwnd)
        # self.root.deiconify()
        self.root.after(150, self.root.destroy)

    def show_root(self, systray):
        # ** show window **
        """
        # * old [
        try:
            systray.shutdown()
        except RuntimeError:
            pass
        # ] *
        """
        self.root.after(150, self.root.deiconify)

    def hide_root(self):
        # ** hide & show window on the system taskbar **
        self.systray.start()
        self.root.withdraw()

    def tray_option(self, systray):
        # ** dynamic tray option Activate/Deactivate **
        self.pressed("a"),
        self.button_state()

    def pressed(self, letter):
        # ** shortcut effect **
        if self.buttons_[letter][0]['fg'] == 'orange':
            self.buttons_[letter][0].config(text="Dea\u0331ctivate", fg='red')
            self.systray.update(menu_options=self.trayDeactivate)  # pull request, github.com/MagTun/infi.systray
        else:
            self.buttons_[letter][0].config(text="A\u0331ctivate", fg='orange')
            self.systray.update(menu_options=self.trayActivate)  # github.com/MagTun/infi.systray/tree/develop/src
        self.buttons_[letter][0].config(relief='sunken', state='active')
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
    reminder = ForgetNot()
    reminder.run()  # keep window 'alive'


if __name__ == '__main__':
    main()  # executed only from forgetnot.py
