# import all necessary functions
from tkinter import *
from random import choice
import sys
import os
import json


"""
** Dice20 **
* A Python simple dice20 roll simulation for fun.
* You forgot your special dice20 and you can't play your favorite game with your friends?
* Then this is for you!
* Simple gui using Python and Tkinter module to represent a virtual dice20.
* Player can press "Roll!":button or <r>:key for a random outcome. 
"""


class Dice20:
    """ initialize properties """
    def __init__(self):
        self.root = Tk()  # main window
        self.root.title("Dice20")  # window title
        self.root.geometry('267x267')  # window size
        self.root.resizable(False, False)  # no resizable window
        self.root.config(bg='#232323')  # window background color in hex
        # JSON file
        with open(self.resource_path("data.json"), "r") as f:
            self.dice_faces = json.load(f)
        self.bgIcon = PhotoImage(data=self.dice_faces["bgIcon.png"])  # parse image data
        self.root.iconphoto(False, self.bgIcon)  # window icon

        # decode dice20 faces
        for k in range(1, 20+1):
            self.dice_faces[f'bgDice{k}.png'] = PhotoImage(data=self.dice_faces[f'bgDice{k}.png'].encode('utf8'))

        # Add background images
        self.bgDice = self.dice_faces["bgDice20.png"]
        self.bgDragon = PhotoImage(data=self.dice_faces["bgDragon.png"])
        self.bgSword = PhotoImage(data=self.dice_faces["bgSword.png"])

        # Create canvas
        self.canvasDragon = Canvas(self.root, width=254, height=154, bg='#000000', highlightbackground='#09446e')
        self.canvasDragon.pack(pady=7)
        self.canvasDice = Canvas(self.root, width=61, height=69, bg='#020002', highlightthickness=0)
        self.canvasDice.pack()
        self.canvasSword = Canvas(self.root, width=254, height=72, bg='#000000', highlightbackground='#194e4e')
        self.canvasSword.pack()

        # Display images
        self.containerDragon = self.canvasDragon.create_image(0, 0, image=self.bgDragon, anchor='nw')
        self.containerDice = self.canvasDice.create_image(0, 0, image=self.bgDice, anchor='nw')
        self.containerSword = self.canvasSword.create_image(0, 13, image=self.bgSword, anchor='nw')

        # button style
        self.button = Button(self.canvasSword, text="Roll!", font='times', width=7, height=3, bg='#000000',
                             fg='#b22d17', activebackground='#09446e', command=self.roll)
        self.button.pack()

        # more secrets..
        self.dragonEye = Frame(self.canvasDragon, bg='#b22d17', width=1, height=1)
        self.dragonEye.place(x=122, y=67)

        # Create window canvas
        self.windowDice = self.canvasDragon.create_window(23, 20, anchor='nw', window=self.canvasDice)
        self.windowSwordButton = self.canvasSword.create_window(183, 3, anchor='nw', window=self.button)

        # shortcut key label properties
        self.shortcut_label = Label(self.root, text='', fg='#a6acf9', bg='#232323', font='times 9', anchor='center')

        # bind keyboard shortcut
        self.root.bind('<r>', self.roll)

        # bind button hover
        self.button.bind('<Enter>', self.button_hover)
        self.dragonEye.bind('<Leave>', self.button_hover)

        # keep window visible
        self.mainloop = self.root.mainloop

    """ methods """

    # absolute path to resource, works for dev and for PyInstaller
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    # dice roll picker
    def roll(self, event=None):
        # <r>:shortcut key and button animation
        if event:
            self.button.config(relief='sunken', state='active')
            self.button.after(150, lambda: self.button.config(relief='raised', state='normal'))
        # dice outcome
        face = choice(range(1, 20+1))
        self.canvasDice.itemconfig(self.containerDice, image=self.dice_faces[f'bgDice{face}.png'])

    # display shortcut key option
    def button_hover(self, event):
        if str(event)[1] == "L":
            self.shortcut_label.config(text="Draco Dormiens Nunquam Titillandus", fg='red')
            self.shortcut_label.pack(fill='x', side='bottom')
            # clear shortcut key display
            self.shortcut_label.after(3000, lambda: self.shortcut_label.config(text='Good Luck Master!', fg='#1d6fc4'))
        else:
            if self.shortcut_label['fg'] in '#1d6fc4red':
                pass
            else:
                self.shortcut_label.config(text="github.com/fireltom/PySimple             Shortcut: R")
                # clear shortcut key display
                self.shortcut_label.after(3000, lambda: self.shortcut_label.config(text=''))
            self.shortcut_label.pack(fill='x', side='top')


# execute dice20
dice20 = Dice20()
# keep dice20 window 'alive'
dice20.mainloop()
