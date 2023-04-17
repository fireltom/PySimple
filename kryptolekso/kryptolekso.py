# import all necessary modules
from tkinter import Tk, Label, Text, StringVar, Entry, Frame, Button, messagebox, Menu
from cryptography.fernet import Fernet
import sys
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename


"""
** Kryptolekso **
* A Python simple "Secret Message Encryption-Decryption" tool.
* You are bored and you want to try something new?
* Message to your crush (girlfriend / boyfriend) at any time, without fear of reading this message by anyone else! 
* Simple gui with Python, using Tkinter & fernet cryptography modules to represent an encryption-decryption tool.
* User can press buttons or try keyboard shortcuts for ease and convenience.
 """


class Kryptolekso:
    # *** class attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * window properties *
        self.root = Tk()  # main window
        self.root.title("Kryptolekso")
        self.root.geometry('376x421')
        self.root.resizable(False, False)
        self.root.config(bg='#09446e')
        # self.icon = PhotoImage(data=self.image_data())  # parse image data, old
        # self.root.iconphoto(False, self.icon)  # old
        self.ico = self.resource_path("kryptolekso.ico")
        self.root.iconbitmap(self.ico)

        # * variables *
        self.code = StringVar()  # store secret-key
        self.cipherSuite = None  # key container

        # * labels & user inputs *
        self.label = Label(self.root, text="Enter Text For Encryption & Decryption", font='Arial 10 bold',
                           fg='#a6a6ff', bg='#09446e')
        self.label.pack(pady=2)
        self.text = Text(self.root, font='Arial 12 bold', width=39, height=7, fg='#a6acf9', bg='#232323',
                         relief='groove', wrap='word', bd=2)
        self.text.pack(pady=2)
        self.label2 = Label(self.root, text="\nEnter Secret-Key For Encryption & Decryption", font='Arial 10 bold',
                            fg='#a6a6ff', bg='#09446e')
        self.label2.pack(pady=2)
        self.entry = Entry(self.root, textvariable=self.code, font='Arial 10 bold', width=50, fg='black', bg='#a6acf9',
                           bd=2)
        self.entry.pack(pady=2)

        # * buttons *
        self.frame = Frame(self.root, bg='#09446e')
        self.frame.pack(pady=8)
        self.button_encrypt = Button(self.frame, text="E\u0331NCRYPT", font='Arial 12 bold', width=10, fg='#a6acf9',
                                     bg='#121212', activebackground='#125d9a', bd=2, command=self.encryption)
        self.button_encrypt.pack(side='left', padx=2, pady=2)
        self.button_decrypt = Button(self.frame, text="D\u0331ECRYPT", font='Arial 12 bold', width=10, fg='#3697f5',
                                     bg='#121212', activebackground='#125d9a', bd=2, command=self.decryption)
        self.button_decrypt.pack(side='left', padx=2, pady=2)
        self.button_clear = Button(self.frame, text="C\u0331LEAR", font='Arial 12 bold', width=10, fg='#b94323',
                                   bg='#121212', activebackground='#125d9a', bd=2, command=self.clear)
        self.button_clear.pack(side='right', padx=2, pady=2)
        self.frame2 = Frame(self.root, bg='#09446e')
        self.frame2.pack(pady=16)
        self.button_generate = Button(self.frame2, text="G\u0331enerate Key (Hold Alt & Press)", font='Arial 12 bold',
                                      width=34, fg='#b94323', bg='#121212', activebackground='#125d9a', bd=2)
        self.button_generate.pack(side='top', padx=2, pady=2)
        self.button_load = Button(self.frame2, text="L\u0331oad Key", font='Arial 13 bold', width=16, fg='orange',
                                  bg="#121212", activebackground='#125d9a', bd=2, command=self.load_key)
        self.button_load.pack(side='left', padx=2, pady=2)
        self.button_save = Button(self.frame2, text="S\u0331ave Key", font='Arial 13 bold', width=16, fg='orange',
                                  bg='#121212', activebackground='#125d9a', bd=2, command=self.save_key)
        self.button_save.pack(side='right', padx=2, pady=2)

        # * about *
        self.label3 = Label(self.root, text="github.com/fireltom/PySimple", font='Arial 10 bold',
                            fg='#a6a6ff', bg='#09446e')
        self.label3.pack()

        # * buttons dictionary *
        self.buttons_ = {
                        "e": (self.button_encrypt, self.encryption),
                        "d": (self.button_decrypt, self.decryption),
                        "c": (self.button_clear, self.clear),
                        "g": (self.button_generate, self.generate_key),
                        "l": (self.button_load, self.load_key),
                        "s": (self.button_save, self.save_key),
        }

        self.button_generate.bind('<Alt-Button-1>',
                                  lambda event: [self.pressed("g"), self.buttons_["g"][1]()])  # special press

        # * shortcuts *
        for key in self.buttons_.keys():
            self.root.bind(f'<Alt-{key}>', lambda event: [self.pressed(event.char), self.buttons_[event.char][1]()])

        # * mouse menu *
        self.text.bind("<Button-3>", self.mouse_menu)
        self.entry.bind("<Button-3>", self.mouse_menu)

    # *** methods ***

    def generate_key(self):
        # ** generate key for encryption & decryption **
        key = Fernet.generate_key()
        self.code.set(key.decode())  # binary 'key' to string
        self.cipherSuite = Fernet(key)

    def encryption(self):
        # ** encrypt message **
        key = self.code.get()  # check for key
        if key:
            message = self.text.get(1.0, 'end-1c')  # user text
            if message:  # check blank message
                encoded = message.encode('utf8', 'ignore')  # string to binary, 'ignore' errors
                if encoded:  # check encode
                    try:
                        ciphers = self.cipherSuite.encrypt(encoded)
                    except Exception:
                        ciphers = None
                        messagebox.showerror("Encryption", "Invalid Key")
                    self.text.delete(1.0, 'end')
                    if ciphers:
                        self.text.insert(1.0, ciphers)
                else:
                    messagebox.showerror("Encryption", "Invalid Characters")
        else:  # no key
            messagebox.showerror("Encryption", "Enter Secret-key!")

    def decryption(self):
        # ** decrypt message **
        key = self.code.get()
        if key:
            ciphers = self.text.get(1.0, 'end')  # ciphers to decrypt
            if ciphers:  # check blank decryption
                try:
                    encoded = self.cipherSuite.decrypt(ciphers)
                except Exception:
                    encoded = None
                    messagebox.showerror("Decryption", "Invalid Key or Message")
                self.text.delete(1.0, 'end')
                if encoded:
                    message = encoded.decode('utf8', 'ignore')  # binary to string, 'ignore errors'
                    self.text.insert(1.0, message)
                else:
                    messagebox.showerror("Decryption", "Invalid Characters")
        else:
            messagebox.showerror("Decryption", "Enter Secret-key!")

    def clear(self):
        # ** clear text inputs **
        self.text.delete(1.0, 'end')

    def load_key(self):
        # ** load key from file **
        file_name = askopenfilename(
                    defaultextension=".txt",
                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file_name == "":
            pass
        else:
            with open(file_name, 'r') as file:
                self.code.set(file.read())

    def save_key(self):
        # ** save key to file **
        key = self.code.get()
        if key:
            file_name = asksaveasfilename(
                        initialfile='Untitled.txt', defaultextension=".txt",
                        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if file_name == "":
                pass
            else:
                with open(file_name, 'w') as file:
                    file.write(key)

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

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** keep window visible **
        self.root.mainloop()


def main():
    kryptolekso = Kryptolekso()
    kryptolekso.run()  # keep Kryptolekso window 'alive'


if __name__ == "__main__":
    main()  # executed only from kryptolekso.py
    # print("\033[2;31;40m Bright Red") # test
    # print(Kryptolekso.__doc__)  # test
