# import all necessary modules
from tkinter import Tk, Frame, Label, Button
import sys
import os


"""
** pyCalculator **
* A Python simple calculator for a change.
* You are bored and you want to try something new?
* Then this is for you!
* Simple gui using Python and Tkinter module to represent a virtual calculator.
* User can press buttons or try numpad shortcuts. 
"""


class Calculator:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("pyCalculator")  # window title
        self.root.geometry('363x522')
        self.root.config(bg='#09446e')  # window color, samples: '#7067fd', '#09446e'
        self.root.resizable(False, False)
        self.ico = self.resource_path("pycalculator.ico")
        self.root.iconbitmap(self.ico)
        self.borderColor = Frame(self.root, bg='#a6acf9')  # calculation screen border
        self.borderColor.grid(padx=10, pady=5, columnspan=5)  # border position
        # self.root.attributes('-alpha', 0.5)  # test
        # self.root.attributes('-transparentcolor', '#232323')  # test
        # self.root.overrideredirect(1)  # test

        # * variables *
        self.displayValue = "0"
        self.result = "0"
        self.squareRoot = False

        # * screen text properties *
        self.label = Label(self.borderColor, text=self.displayValue, font='Arial 28 bold', anchor='nw', width=14,
                           height=2, bg='#232323', fg='#a6acf9', bd='0', justify='left')
        self.label.pack(padx=1, pady=1)

        # * calculator buttons *
        # buttons: "1", "2", "3", "+"
        self.btn1 = Button(self.root, text="1", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(1))
        self.btn1.grid(padx=(5, 0), row=2, column=1)
        self.btn2 = Button(self.root, text="2", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(2))
        self.btn2.grid(row=2, column=2)
        self.btn3 = Button(self.root, text="3", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(3))
        self.btn3.grid(row=2, column=3)
        self.btnAdd = Button(self.root, text="+", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display('+'))
        self.btnAdd.grid(row=2, column=4)

        # buttons: "4", "5", "6", "-"
        self.btn4 = Button(self.root, text="4", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(4))
        self.btn4.grid(padx=(5, 0), row=3, column=1)
        self.btn5 = Button(self.root, text="5", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(5))
        self.btn5.grid(row=3, column=2)
        self.btn6 = Button(self.root, text="6", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(6))
        self.btn6.grid(row=3, column=3)
        self.btnMin = Button(self.root, text="-", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display('-'))
        self.btnMin.grid(row=3, column=4)

        # buttons: "7", "8", "9", "*"
        self.btn7 = Button(self.root, text="7", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(7))
        self.btn7.grid(padx=(5, 0), row=4, column=1)
        self.btn8 = Button(self.root, text="8", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(8))
        self.btn8.grid(row=4, column=2)
        self.btn9 = Button(self.root, text="9", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(9))
        self.btn9.grid(row=4, column=3)
        self.btnMul = Button(self.root, text="*", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display('*'))
        self.btnMul.grid(row=4, column=4)

        # buttons: "(", "0", ".", "/"
        self.btnLPar = Button(self.root, text="(", font='Arial 16 bold', width=6, height=2, bg='#121212',
                              fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display("("))
        self.btnLPar.grid(padx=(5, 0), row=5, column=1)
        self.btn0 = Button(self.root, text="0", font='Arial 16 bold', width=6, height=2, bg='#121212',
                           fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(0))
        self.btn0.grid(row=5, column=2)
        self.btnCom = Button(self.root, text=".", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display('.'))
        self.btnCom.grid(row=5, column=3)
        self.btnDiv = Button(self.root, text="/", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display('/'))
        self.btnDiv.grid(row=5, column=4)

        # buttons: "%", "^", ":√", ")"
        self.btnPer = Button(self.root, text="%", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=self.percentage)
        self.btnPer.grid(row=6, column=4)
        self.btnPow = Button(self.root, text="^", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display('**'))
        self.btnPow.grid(row=6, column=3)
        self.btnSqr = Button(self.root, text="√", font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#3697f5', activebackground='#125d9a', command=lambda: self.display(':√', True))
        self.btnSqr.grid(row=6, column=2)
        self.btnRPar = Button(self.root, text=")", font='Arial 16 bold', width=6, height=2, bg='#121212',
                              fg='#a6acf9', activebackground='#125d9a', command=lambda: self.display(")"))
        self.btnRPar.grid(padx=(5, 0), row=6, column=1)

        # buttons: "AC", "Copy", "←", "="
        self.btnAC = Button(self.root, text="AC", font='Arial 16 bold', width=6, height=2, bg='#121212',
                            fg='#b94323', activebackground='#125d9a', command=self.clear)
        self.btnAC.grid(padx=(5, 0), row=7, column=1)
        self.btnCp = Button(self.root, text="Copy", font='Arial 16 bold', width=6, height=2, bg='#121212',
                            fg='orange', activebackground='#125d9a', command=self.clipboard)
        self.btnCp.grid(row=7, column=2)
        self.btnRet = Button(self.root, text='←', font='Arial 16 bold', width=6, height=2, bg='#121212',
                             fg='#b94323', activebackground='#125d9a', command=self.backspace)
        self.btnRet.grid(row=7, column=3)
        self.btnEq = Button(self.root, text="=", font='Arial 16 bold', width=6, height=2, bg='#121212',
                            fg='orange', activebackground='#125d9a', command=self.solve)
        self.btnEq.grid(row=7, column=4)

        self.label2 = Label(self.root, text="github.com/fireltom/PySimple", font='Arial 9 bold', bg='#09446e',
                            fg='#a6acf9')
        self.label2.grid(columnspan=5)

        # * buttons dictionary *
        self.buttons = {
                        "1": self.btn1,
                        "2": self.btn2,
                        "3": self.btn3,
                        "+": self.btnAdd,
                        "4": self.btn4,
                        "5": self.btn5,
                        "6": self.btn6,
                        "-": self.btnMin,
                        "7": self.btn7,
                        "8": self.btn8,
                        "9": self.btn9,
                        "*": self.btnMul,
                        "(": self.btnLPar,
                        "0": self.btn0,
                        ".": self.btnCom,
                        "/": self.btnDiv,
                        "^": self.btnPow,
                        "&": self.btnSqr,
                        ")": self.btnRPar,
        }

        # * buttons keyboard shortcuts *
        self.root.bind('<Key-1>', lambda event: [self.display("1"), self.pressed("1")])
        self.root.bind('<Key-2>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-3>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<+>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-4>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-5>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-6>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<minus>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-7>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-8>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<Key-9>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<*>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<(>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<.>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('</>', lambda event: [self.display(event.char), self.pressed(event.char)])
        self.root.bind('<)>', lambda event: [self.display(event.char), self.pressed(event.char)])

        self.root.bind('<^>', lambda event: [self.display("**"), self.pressed(event.char)])
        self.root.bind('<&>', lambda event: [self.display(":√", True), self.pressed(event.char)])
        # different approach
        self.root.bind('<Key-0>', lambda event: [self.display(event.char),
                                                 self.btn0.config(relief='sunken', state='active'),
                                                 self.btn0.after(150, lambda: self.btn0.config(relief='raised',
                                                                                               state='normal'))])
        self.root.bind('<%>', self.percentage)
        self.root.bind('<Delete>', self.clear)
        self.root.bind('<Control-c>', self.clipboard)
        self.root.bind('<BackSpace>', self.backspace)
        self.root.bind('<Return>', self.solve)

    """ Methods """

    def display(self, value, root=False):
        # ** user inputs **
        if root:
            self.squareRoot = True
        result = False
        if '\n' in self.displayValue and str(value) in "0123456789(":  # special case: 'result', 'Invalid' or '0'
            result = True
        if result or self.displayValue == "Invalid" or self.displayValue == "0" and str(value) in "0123456789(√":
            self.displayValue = str(value)
        elif str(value) in "*/." and self.displayValue[-1] in "*/.":  # duplicate operator protect
            pass
        elif '\n' in self.displayValue:  # new calculation
            self.displayValue = str(self.result) + str(value)
        else:
            self.displayValue += str(value)
        self.label.config(text=self.displayValue)

    def clear(self, event=None):
        # ** clear screen **
        self.displayValue = "0"
        self.label.config(text=self.displayValue)
        if event:  # shortcut effect
            self.btnAC.config(relief='sunken', state='active')
            self.btnAC.after(150, lambda: self.btnAC.config(relief='raised', state='normal'))

    def solve(self, event=None, per=None):
        # ** calculation result **
        result = self.displayValue
        if self.squareRoot:
            self.squareRoot = False
            result = result.replace(":√", "**(1/2)")
        try:
            self.result = eval(result)
            if isinstance(self.result, float):  # special case: float presentation to integer
                if self.result == int(self.result):
                    self.result = int(self.result)
                else:
                    self.result = round(self.result, 9)
            if per:
                self.displayValue = str(self.result) + '\n'
            else:
                self.displayValue = f'{str(self.result)}\n{self.displayValue}'
        except Exception:
            self.displayValue = "Invalid"
        self.label.config(text=self.displayValue)
        if event:  # shortcut effect
            self.btnEq.config(relief='sunken', state='active')
            self.btnEq.after(150, lambda: self.btnEq.config(relief='raised', state='normal'))

    def backspace(self, event=None):
        # ** screen backspace  **
        if self.displayValue in "0Invalid()+-*/":  # special case: screen 'zeroing'
            self.displayValue = "0"
        else:
            if '\n' in self.displayValue:  # special case: result and calculation
                start = 0
                for index in range(len(self.displayValue)):
                    if self.displayValue[index] == '\n':
                        start = index
                        break
                # * delete user last input *
                self.displayValue = self.displayValue[start+1:]
            self.displayValue = self.displayValue[:-1]
        self.label.config(text=self.displayValue)
        if event:  # shortcut effect
            self.btnRet.config(relief='sunken', state='active')
            self.btnRet.after(150, lambda: self.btnRet.config(relief='raised', state='normal'))

    def percentage(self, event=None):
        # ** percentage calculation **
        k = -1
        temp = self.displayValue
        self.solve()
        if self.displayValue == "Invalid":
            return
        self.displayValue = temp
        # * detect percentage case: '+', '-', '*', '/' *
        if "+" in self.displayValue or "-" in self.displayValue or "*" in self.displayValue \
                or "/" in self.displayValue:
            while k >= -len(self.displayValue) and self.displayValue[k] not in "+-*/":
                k += -1
            whole = self.displayValue[:k]
            part = self.displayValue[k+1:]
            per = "0"
            if self.displayValue[k] == "+":
                per = f'{whole} * {part}/100 + {whole}'
            elif self.displayValue[k] == "-":
                per = f'{whole} - {whole} * {part}/100'
            elif self.displayValue[k] == "*":
                per = f'{whole} * {part}/100'
            elif self.displayValue[k] == "/":
                per = f'{whole} / {part} * 100'
            self.displayValue = per
            self.solve(per=True)
        if event:  # shortcut effect
            self.btnPer.config(relief='sunken', state='active')
            self.btnPer.after(150, lambda: self.btnPer.config(relief='raised', state='normal'))

    def clipboard(self, event=None):
        # ** copy calculation **
        self.root.clipboard_clear()
        self.root.clipboard_append(self.displayValue)
        if event:  # shortcut effect
            self.btnCp.config(relief='sunken', state='active')
            self.btnCp.after(150, lambda: self.btnCp.config(relief='raised', state='normal'))

    def pressed(self, index):
        # ** rest keyboard shortcuts effect  **
        self.buttons[index].config(relief='sunken', state='active')
        self.buttons[index].after(150, lambda: self.buttons[index].config(relief='raised', state='normal'))

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** keep window visible **
        self.root.mainloop()


def main():
    # ** run Calculator instance **
    calculator = Calculator()
    calculator.run()  # keep calculator window 'alive'


if __name__ == '__main__':
    main()  # executed only from pycalculator.py
