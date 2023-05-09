# import all necessary functions
from tkinter import Tk, PhotoImage, Button
import random
import sys
import os


"""
** DiceRoll **
* A Python simple dice roll simulation for fun.
* You forgot/lost your pair of regular dices and you cant play your favorite game with your friends?
* Then this is for you!
* Simple gui with Python, using Tkinter module to represent two virtual dices.
* User can press dice window or try <r> shortcut for ease and convenience. 
"""


class DiceRoll:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("Dice Roll")  # window title
        self.root.geometry('304x304')  # window size
        self.root.resizable(False, False)  # no resizable window
        self.root.config(bg='black')  # window color in hex
        self.ico = self.resource_path("diceroll.ico")  # script icon
        self.root.iconbitmap(self.ico)
        self.bg = PhotoImage(file=self.resource_path("dicerollbg.png"))  # background image

        # window button style
        self.button_roll = Button(self.root, text="\u2681    \n    \u2685", font='Arial 110 bold', bg='#13a6f9',
                                  fg='black', highlightthickness=0, bd=0, image=self.bg, compound='center',
                                  activeforeground='black', command=self.roll)
        self.button_roll.pack()
        self.button_roll.focus_set()  # set focus

        # * buttons dictionary *
        self.buttons_ = {
                        "r": (self.button_roll, self.roll),
                        "R": (self.button_roll, self.roll)
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<{key}>', lambda event: (self.pressed(event.char), self.buttons_[event.char][1]()))

    # """ Methods """

    def roll(self):
        # ** dice roll picker **
        dice = ['\u2681', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']  # dice six 'faces'
        self.button_roll.config(text=f'{random.choice(dice)}    \n    {random.choice(dice)}')  # shuffle dice dots

    def pressed(self, letter):
        # ** shortcut effect **
        self.buttons_[letter][0].config(relief='sunken', state='active')
        self.buttons_[letter][0].after(150, lambda: self.buttons_[letter][0].config(relief='raised', state='normal'))

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** keep window visible **
        self.root.mainloop()


def main():
    dice = DiceRoll()  # DiceRoll instance
    dice.run()


if __name__ == '__main__':
    main()  # executed only from diceroll.py
