# import all necessary modules
from tkinter import Tk, PhotoImage, Canvas, Label, Entry, StringVar, Button, Menu
from tkinter.filedialog import askopenfilename, askdirectory
import sys
import os
import fnmatch
from shutil import rmtree
from pikepdf import Pdf  # Fix importlib_metadata.version not working properly with PyInstaller: -->
# --> https://github.com/pikepdf/pikepdf/pull/358


"""
** iLovePdf **
* A Python simple pdf tool.
* Do you ever find yourself bored with online pdf-file handlers and bad advertising?
* Then this is for you!
* Simple gui with Python, using pikepdf & Tkinter modules to help you merge & split your pdf files.
* User can press buttons or try <Alt + 'key'> shortcuts for ease and convenience.
"""


class IlovePdf:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("iLovePdf")
        self.root.geometry('386x210')
        self.root.resizable(False, False)
        self.root.config(bg='#136799')
        self.bg = PhotoImage(file=self.resource_path("ilovepdfbg.png"))  # background image
        self.ico = self.resource_path("ilovepdf.ico")
        self.root.iconbitmap(self.ico)

        # * variables *
        self.path = StringVar()
        self.path.trace_add('write',
                            lambda var, index, mode: [self.check_entry(), self.entry.xview_moveto(1)])  # trace entry
        self.action = 0  # 1 --> Split, 2 --> Merge
        self.pdfName = ''
        self.nwd = ''  # new working dir
        self.pdf_list = []  # list of pdf files, in cwd
        # print(str(dir(Entry)).replace(" ",'\n'))  # test

        # * canvas, entry & buttons *
        self.canvas_bg = Canvas(self.root, bg='black')  # , highlightbackground="136799")  # test
        self.canvas_bg.pack()
        self.canvas_bg.create_image(0, 0, anchor='nw', image=self.bg)
        # *
        self.label = Label(self.canvas_bg, text='', bg='black', highlightthickness=0, bd=0)
        self.label.pack(pady=10, anchor='w')
        self.canvas_bg.create_text(186, 25, text="~ iLovePdf ~", fill='#a6a6f9', font='Arial 13 bold')
        self.entry = Entry(self.canvas_bg, textvariable=self.path, font='Arial 12 bold', width=40, fg='black',
                           bg='#a6a6f9', bd=2)
        self.entry.pack(padx=8, pady=8)
        # *
        self.canvas_bg.create_text(224, 94, text="Open folder with Pdf files for merging!",
                                   fill='#a6a6f9', font='Arial 10 bold')
        self.button_dir = Button(self.canvas_bg, text="M\u0331erge", font='Arial 10 bold', width=9,
                                 fg='#3697f5', bg='#040404', activebackground='#125d9a', bd=2, command=self.load_dir)
        self.button_dir.pack(padx=8, pady=4, anchor='w')
        # *
        self.canvas_bg.create_text(172, 130, text="Select Pdf file to split!",
                                   fill='#a6a6f9', font='Arial 10 bold')
        self.button_filepath = Button(self.canvas_bg, text="S\u0331plit", font='Arial 10 bold', width=9,
                                      fg='#b94323', bg='#040404', activebackground='#125d9a', bd=2,
                                      command=self.load_pdf)
        self.button_filepath.pack(padx=8, pady=4, anchor='w')
        # *
        self.button_convert = Button(self.canvas_bg, text="Convert", font='Arial 10 bold', width=9,
                                     fg='orange', bg='#040404', activebackground='#125d9a', bd=2,
                                     command=self.convert_pdf)
        self.button_convert.pack(pady=8)
        # *
        self.label2 = Label(self.canvas_bg, text='', bg='black', highlightthickness=0, bd=0)
        self.label2.pack(anchor='w')
        self.canvas_bg.create_text(194, 196, text="github.com/fireltom/PySimple", fill='#6a6af9', font='Arial 8 bold')

        # * buttons dictionary *
        self.buttons_ = {
                        "m": (self.button_dir, self.load_pdf),
                        "s": (self.button_filepath, self.load_dir),
                        "i": (self.button_convert, self.convert_pdf),
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: (self.pressed(event.char), self.buttons_[event.char][1]()))

        # * mouse menu *
        self.entry.bind("<Button-3>", self.mouse_menu)

    # *** Methods ***

    def load_pdf(self):
        # ** load pdf-file for splitting **
        file = askopenfilename(
            defaultextension=".pdf",
            filetypes=(("PDF", "*.pdf"), ("All Files", "*.*"))
        )
        if not file:
            pass
        else:
            self.path.set(file)  # load path
            # self.entry.xview_moveto(1)  # old

    def load_dir(self):
        # ** load pdf-file folder for merging **
        folder = askdirectory()
        if not folder:
            pass
        else:
            self.path.set(folder)

    def convert_pdf(self):
        # ** convert pdf-file **
        if self.action == 1:  # split
            self.action = 0
            file = self.entry.get()
            try:
                isDone = os.path.isdir(self.nwd)
                if not isDone:
                    os.mkdir(self.nwd)  # output dir
                old_pdf = Pdf.open(file)
                for number, page in enumerate(old_pdf.pages):
                    new_pdf = Pdf.new()
                    new_pdf.pages.append(page)
                    name = self.pdfName + "_" + str(number+1) + ".pdf"
                    path = os.path.join(self.nwd, name)
                    new_pdf.save(path)
                self.button_convert.config(text="Done!", fg='#b94323')
                self.action = 0
            except Exception:
                self.button_convert.config(text="Error!", fg='red')
                self.action = 0
                if self.nwd:
                    rmtree(self.nwd)  # on error, delete any output
        elif self.action == 2:  # merge
            self.action = 0
            cwd = self.entry.get()
            try:
                new_pdf = Pdf.new()
                for name in self.pdf_list:
                    pdf = os.path.join(cwd, name)
                    old_pdf = Pdf.open(pdf)
                    new_pdf.pages.extend(old_pdf.pages)
                isDone = os.path.isdir(self.nwd)
                if not isDone:
                    os.mkdir(self.nwd)
                name = self.pdfName + ".pdf"
                path = os.path.join(self.nwd, name)
                new_pdf.save(path)
                self.pdf_list.clear()
                self.button_convert.config(text="Done!", fg='#3697f5')
                self.action = 0
            except Exception:
                self.button_convert.config(text="Error!", fg='red')
                self.action = 0
                if self.nwd:
                    rmtree(self.nwd)

    def check_entry(self):
        # ** check for valid entry **
        entry = self.entry.get()
        isDir = os.path.isdir(entry)
        isFile = os.path.isfile(entry)
        if isFile:  # check for splitting
            fileName = os.path.splitext(os.path.basename(entry))[0]
            self.pdfName = fileName
            folderName = fileName + "_split"
            cwd = os.path.dirname(entry)
            self.nwd = os.path.join(cwd, folderName)
            fileName += "_1.pdf"
            perhapsDone = os.path.join(self.nwd, fileName)
            isDone = os.path.isfile(perhapsDone)
            if not isDone:
                self.button_convert.config(text="i\u0330Split", fg='#b94323')
                self.action = 1
            else:
                self.button_convert.config(text="Done!", fg='#b94323')
        elif isDir:  # check for merging
            dir_list = os.listdir(entry)
            self.pdf_list = fnmatch.filter(dir_list, '*.pdf')
            if self.pdf_list:  # check if folder is pdf empty
                fileName = self.pdf_list[0].split(".pdf")[0]
                self.pdfName = fileName
                folderName = fileName + "_merge"
                cwd = entry
                self.nwd = os.path.join(cwd, folderName)
                fileName += ".pdf"
                perhapsDone = os.path.join(self.nwd, fileName).replace("/", "\\")
                isDone = os.path.isfile(perhapsDone)
                if not isDone:
                    self.button_convert.config(text="i\u0330Merge", fg='#3697f5')
                    self.action = 2
                else:
                    self.button_convert.config(text="Done!", fg='#3697f5')
            else:
                self.button_convert.config(text="Empty..", fg='#3697f5')
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
    ilikepdf = IlovePdf()
    ilikepdf.run()  # keep window 'alive'


if __name__ == '__main__':
    main()  # executed only from ilovepdf.py
