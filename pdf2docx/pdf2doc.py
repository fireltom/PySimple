# import all necessary modules
from tkinter import Tk, PhotoImage, Canvas, Label, Entry, StringVar, Button, Menu
from tkinter.filedialog import askopenfilename
import sys
import os
from shutil import rmtree
from pdf2docx import parse
from docx2pdf import convert


"""
** Pdf2Docx **
* A Python simple pdf tool.
* Do you ever find yourself bored with online pdf-file handlers and bad advertising?
* Then this is for you!
* Simple gui with Python, using pdf2docx & Tkinter modules to help you convert your pdf & docx files.
* User can press buttons or try <Alt + 'key'> shortcuts for ease and convenience.
* --> Convert .docx to .pdf on Windows or macOS directly using Microsoft Word (must be installed). <--
"""


class Pdf2Doc:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("Pdf2Docx")
        self.root.geometry('386x210')
        self.root.resizable(False, False)
        self.root.config(bg='#136799')
        self.bg = PhotoImage(file=self.resource_path("pdf2docbg.png"))  # background image
        self.ico = self.resource_path("pdf2doc.ico")
        self.root.iconbitmap(self.ico)

        # * variables *
        self.path = StringVar()
        self.path.trace_add('write',
                            lambda var, index, mode: [self.check_entry(), self.entry.xview_moveto(1)])  # trace entry
        self.action = 0  # 1 --> pdf to docx, 2 --> docx to pdf
        self.fileName = ''
        self.nwd = ''  # new working dir
        # print(str(dir(Entry)).replace(" ",'\n'))  # test

        # * canvas, entry & buttons *
        self.canvas_bg = Canvas(self.root, bg='black')  # , highlightbackground="136799")  # test
        self.canvas_bg.pack()
        self.canvas_bg.create_image(0, 0, anchor='nw', image=self.bg)
        # *
        self.label = Label(self.canvas_bg, text='', bg='black', highlightthickness=0, bd=0)
        self.label.pack(pady=10, anchor='w')
        self.canvas_bg.create_text(186, 25, text="~ Pdf2Docx ~", fill='#6aa6f9', font='Arial 13 bold')
        self.entry = Entry(self.canvas_bg, textvariable=self.path, font='Arial 12 bold', width=40, fg='black',
                           bg='#a6a6f9', bd=2)
        self.entry.pack(padx=8, pady=8)
        # *
        self.canvas_bg.create_text(175, 94, text="Select Pdf file to convert!",
                                   fill='#a6a6f9', font='Arial 10 bold')
        self.button_pdf = Button(self.canvas_bg, text="to D\u0331ocx", font='Arial 10 bold', width=9,
                                 fg='#3697f5', bg='#040404', activebackground='#125d9a', bd=2, command=self.load_pdf)
        self.button_pdf.pack(padx=8, pady=4, anchor='w')
        # *
        self.canvas_bg.create_text(180, 130, text="Select Docx file to convert!",
                                   fill='#a6a6f9', font='Arial 10 bold')
        self.button_docx = Button(self.canvas_bg, text="to P\u0331df", font='Arial 10 bold', width=9, fg='#b94323',
                                  bg='#040404', activebackground='#125d9a', bd=2, command=self.load_docx)
        self.button_docx.pack(padx=8, pady=4, anchor='w')
        # *
        self.button_convert = Button(self.canvas_bg, text="Convert", font='Arial 10 bold', width=9, fg='orange',
                                     bg='#040404', activebackground='#125d9a', bd=2, command=self.convert_input)
        self.button_convert.pack(pady=8)
        # *
        self.label2 = Label(self.canvas_bg, text='', bg='black', highlightthickness=0, bd=0)
        self.label2.pack(anchor='w')
        self.canvas_bg.create_text(194, 196, text="github.com/fireltom/PySimple", fill='#9a9af9', font='Arial 8 bold')

        # * buttons dictionary *
        self.buttons_ = {
                        "d": (self.button_pdf, self.load_pdf),
                        "p": (self.button_docx, self.load_docx),
                        "t": (self.button_convert, self.convert_input),
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: (self.pressed(event.char), self.buttons_[event.char][1]()))

        # * mouse menu *
        self.entry.bind("<Button-3>", self.mouse_menu)

    # *** Methods ***

    def load_pdf(self):
        # ** load .pdf file type **
        file = askopenfilename(
            defaultextension=".pdf",
            filetypes=(("PDF", "*.pdf"), ("All Files", "*.*"))
        )
        if not file:
            pass
        else:
            self.action = 1  # this should be before 'load path'!
            self.path.set(file)  # load path

    def load_docx(self):
        # ** load .docx file type **
        file = askopenfilename(
            defaultextension=".docx",
            filetypes=(("DOCX", "*.docx"), ("All Files", "*.*"))
        )
        if not file:
            pass
        else:
            self.action = 2  # this should be before 'load path'!
            self.path.set(file)  # load path

    def convert_input(self):
        # ** convert pdf-file **
        if self.action == 3:  # to docx
            self.action = 0
            file = self.entry.get()
            try:
                isDone = os.path.isdir(self.nwd)
                if not isDone:
                    os.mkdir(self.nwd)  # output dir
                name = self.fileName + ".docx"
                path = os.path.join(self.nwd, name)
                parse(file, path, start=0, end=None)  # convert & save 'file' (pdf) to 'path' (as .docx)
                self.button_convert.config(text="Done!", fg='#b94323')
            except Exception:
                self.button_convert.config(text="Error!", fg='red')
                rmtree(self.nwd, ignore_errors=True)  # on error, delete any output
        elif self.action == 4:  # to pdf
            self.action = 0
            file = self.entry.get()
            try:
                isDone = os.path.isdir(self.nwd)
                if not isDone:
                    os.mkdir(self.nwd)
                name = self.fileName + ".pdf"
                path = os.path.join(self.nwd, name)
                sys.stderr = open(self.resource_path("consoleoutput.log"), "w")
                convert(file, path)  # convert & save 'file' (docx) to 'path' (as .pdf)
                sys.stderr.close()
                self.button_convert.config(text="Done!", fg='#b94323')
            except Exception:
                self.button_convert.config(text="Error!", fg='red')
                rmtree(self.nwd, ignore_errors=True)

    def check_entry(self):
        # ** check for valid entry **
        entry = self.entry.get()
        isFile = os.path.isfile(entry)
        if isFile:  # check for pdf file
            name = os.path.splitext(os.path.basename(entry))
            if self.action == 1 or name[-1] == ".pdf":
                folder = name[0] + "_2docx"
                self.fileName = name[0]
                cwd = os.path.dirname(entry)
                self.nwd = os.path.join(cwd, folder)
                file = name[0] + ".docx"
                perhapsDone = os.path.join(self.nwd, file)
                isDone = os.path.isfile(perhapsDone)
                if not isDone:
                    self.action = 3  # enable pdf to docx option
                    print(self.action)
                    self.button_convert.config(text="t\u0331o Docx", fg='#3697f5')
                else:
                    self.button_convert.config(text="Already!", fg='#3697f5')
            elif self.action == 2 or name[-1] == ".docx":
                folder = name[0] + "_2pdf"
                self.fileName = name[0]
                cwd = os.path.dirname(entry)
                self.nwd = os.path.join(cwd, folder)
                file = name[0] + ".pdf"
                perhapsDone = os.path.join(self.nwd, file)
                isDone = os.path.isfile(perhapsDone)
                if not isDone:
                    self.action = 4  # enable docx to pdf option
                    self.button_convert.config(text="t\u0331o Pdf", fg='#b94323')
                else:
                    self.button_convert.config(text="Already!", fg='#b94323')
            else:
                self.button_convert.config(text="Convert", fg='orange')
        else:
            self.button_convert.config(text="Convert", fg='orange')

    def pressed(self, letter):
        # ** shortcut effect **
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
    pdf2Doc = Pdf2Doc()
    pdf2Doc.run()  # keep window 'alive'


if __name__ == '__main__':
    main()  # executed only from pdf2doc.py
