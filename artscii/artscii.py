# import all necessary modules
import cv2
from tkinter import Tk, Label, StringVar, Entry, Frame, Button, Menu
from tkinter.filedialog import askopenfilename
import sys
import os


"""
** Artscii **
* A Python simple image to "ascii art" converter.
* Have some cool images and you want to try ascii art for fun?
* Then this is for you!
* Simple gui with Python, using opencv & Tkinter modules to convert an image to text.
* User can press "Load" & "Convert" :buttons or 'Alt + c' & 'Alt + c' :keys for ease and convenience. 
"""


class Stencil:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("Artscii")
        self.root.geometry('390x180')
        self.root.resizable(False, False)
        self.root.config(bg='#205062')
        self.root.iconbitmap(self.resource_path("artscii.ico"))
        # self.root.attributes('-transparentcolor', '#205062')  # test

        # * variables *
        self.load_path = StringVar()  # image source
        self.load_path.trace_add('write', self.check_input)  # trace path
        self.save_path = StringVar()  # image destination

        # * frames, labels & user input *
        """
        #  * test [ 
        # self.bg = PhotoImage(file="bg.png")
        # self.bglabel = Label(self.root, image=self.bg)
        # self.bglabel.place(relx=0.5, rely=0.5, anchor='center')
        #  ] *
        """
        self.frame = Frame(self.root, bg='#205062')
        self.frame.pack(padx=2, pady=2)
        self.label = Label(self.frame, text=f'Choose Image to Convert: {"   "*17}', font='Arial 10 bold',
                           fg='#a6a6ff', bg='#205062')
        self.label.pack(padx=2, pady=2)
        self.frame2 = Frame(self.root, bg='#205062')
        self.frame2.pack(padx=2, pady=2)
        self.entry = Entry(self.frame2, textvariable=self.load_path, font='Arial 10 bold', width=42, fg='black',
                           bg='#a6acff', bd=2)
        self.entry.pack(side='left', padx=2, pady=2)
        self.button_load = Button(self.frame2, text="L\u0331oad", font='Arial 10 bold', width=8, fg='orange',
                                  bg="#121212", activebackground='#125d9a', bd=2, command=self.load_image)
        self.button_load.pack(padx=2, pady=2)
        # *
        self.frame3 = Frame(self.root, bg='#205062')
        self.frame3.pack(padx=2, pady=2)
        self.label2 = Label(self.frame3, text=f'Save Image as ASCII Art:  {"   "*17}', font='Arial 10 bold',
                            fg='#a6a6ff', bg='#205062')
        self.label2.pack(padx=2, pady=2)
        self.frame4 = Frame(self.root, bg='#205062')
        self.frame4.pack(padx=2, pady=2)
        self.label3 = Label(self.frame4, textvariable=self.save_path, anchor='e', font='Arial 10 bold', width=37,
                            fg='black', bg='#a6acff', relief='solid', bd=2)
        self.label3.pack(side='left', padx=2, pady=2)
        self.label4 = Label(self.frame4, text="Ready", font='Arial 10 bold', fg='#a6acff',
                            bg='#121212', width=8, relief='solid', bd=2)
        self.label4.pack(padx=2, pady=2)
        # *
        self.button_convert = Button(self.root, text="C\u0331onvert", font='Arial 10 bold', width=8, fg='orange',
                                     bg="#121212", activebackground='#125d9a', bd=2, command=self.convert_image)
        self.button_convert.pack(padx=2, pady=8)

        # * buttons dictionary *
        self.buttons_ = {
                        "l": (self.button_load, self.load_image),
                        "c": (self.button_convert, self.convert_image),
        }

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: [self.pressed(event.char), self.buttons_[event.char][1]()])

        # * mouse menu *
        self.entry.bind("<Button-3>", self.mouse_menu)

    # *** Methods ***

    def load_image(self):
        # ** load key from file **
        file_name = askopenfilename(
            defaultextension=".png",
            filetypes=(("Image", "*.png *.jpg *.jpeg *.tiff"), ("PNG", "*.png"), ("JPG", "*.jpg"), ("All Files", "*.*"))
        )
        if file_name == "":
            pass
        else:
            self.load_path.set(file_name)  # load path
            self.check_input()  # validate

    def convert_image(self):
        # ** convert image to ascii **
        check = True
        convert = self.check_input(ret=check)
        if convert:
            try:
                # * image to sketch *
                image = cv2.imread(self.entry.get())
                grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                invert = cv2.bitwise_not(grey)
                blur = cv2.GaussianBlur(invert, (21, 21), 0)
                invertedBlur = cv2.bitwise_not(blur)
                sketch = cv2.divide(grey, invertedBlur, scale=256.0)
                # * sketch to ascii *
                height = image.shape[0]
                width = image.shape[1]
                ratio = height/width
                newWidth = 100
                newHeight = int(newWidth * ratio)
                dim = (newWidth, newHeight)
                resizedSketch = cv2.resize(sketch, dim, interpolation=cv2.INTER_AREA)
                characters = []
                for y in range(newHeight):
                    for x in range(newWidth):
                        if resizedSketch[y, x] >= 245:
                            characters.append('"')  # white color
                        else:
                            characters.append(" ")  # sketch color
                characters = "".join(characters)
                pixelCount = len(characters)
                asciiTable = []
                for index in range(0, pixelCount, newWidth):
                    asciiRow = characters[index:index + newWidth]
                    asciiTable.append(asciiRow)
                asciiImage = '\n'.join(asciiTable)
                asciiName = self.save_path.get()
                with open(asciiName, 'w') as f:
                    f.write(asciiImage)
                self.label4.config(text="Done!", fg='#3697f5')  # "Done" Label
            except Exception:
                self.label4.config(text="Error!", fg='#ab0d2e')  # "Error" label
        else:
            isFile = os.path.isfile(self.entry.get())
            if isFile:
                self.label4.config(text="Done!", fg='#3697f5')  # already "Done"

    def pressed(self, letter):
        # ** shortcut effect **
        self.buttons_[letter][0].config(relief='sunken', state='active')
        self.buttons_[letter][0].after(150, lambda: self.buttons_[letter][0].config(relief='raised', state='normal'))

    @staticmethod
    def mouse_menu(event):
        # ** right click menu **
        mouse_menu = Menu(None, tearoff=0, takefocus=0)
        # * menu options *
        for option in ['Cut', 'Copy', 'Paste']:
            mouse_menu.add_command(label=option, command=lambda cmd=option: event.widget.event_generate(f'<<{cmd}>>'))
        mouse_menu.tk_popup(event.x_root, event.y_root, entry='0')

    def check_input(self, var=None, index=None, mode=None, ret=None):
        # ** check for valid inputs **
        oldFile = os.path.isfile(self.save_path.get())
        isFile = os.path.isfile(self.entry.get())
        if isFile:
            if not oldFile:
                self.label4.config(text="Ready", fg='#a6acff')
                imageDir = os.path.dirname(self.entry.get())
                imageName = os.path.splitext(os.path.basename(self.entry.get()))[0]
                """
                # * old [
                extention = True
                imageNameNoExtention = ''
                for letter in imageName[::-1]:
                     if letter == ".":
                         extention = False
                         continue
                     if not extention:
                         imageNameNoExtention += letter
                 imageNameNoExtention = imageNameNoExtention[::-1]
                # ] *
                """
                self.save_path.set(imageDir + "/ascii_" + imageName + ".txt")
                if ret:
                    return True  # inform 'convert_image' method
        else:
            self.save_path.set('')  # no valid input, empty label

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** keep window visible **
        self.root.mainloop()


def main():
    sketchy = Stencil()
    sketchy.run()  # keep sketchy window 'alive'


if __name__ == "__main__":
    main()  # executed only from sketchy.py
