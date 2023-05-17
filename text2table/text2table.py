# import all necessary modules
from infi.systray import SysTrayIcon
from tkinter.filedialog import askopenfilename
import sys
import os.path


"""
** Text2table **
* A Python simple text tool.
* Organize your .txt file data to a table like structure!
* Simple tray app with Python, using infi.systray module.
* User can press:
* <Open>: "Open user .txt file."
* <Convert>: "Create new .txt file with user data organized in a table like structure!"
* <Quit>: "Quit app."  
* options from taskbar icon!
"""


class Text2table:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * taskbar properties *
        self.title = "Text2table"
        self.ico = self.resource_path("text2table.ico")
        self.trayConvert = ((self.title, None, lambda systray: None),
                            ("Open", None, lambda systray: self.pick_file_fn()),
                            ("Convert", None, lambda systray: self.check_file_fn(convert=True)))  # tray
        self.trayAlready = ((self.title, None, lambda systray: None),
                            ("Open", None, lambda systray: self.pick_file_fn()),
                            ("Already!", None, lambda systray: None))  # options

        # * variables *
        self.path = ['', '']

        # * tray *
        self.systray = SysTrayIcon(self.ico, self.title, self.trayConvert)

    # *** Methods ***

    def pick_file_fn(self):
        # ** load text file **
        file = askopenfilename(
            defaultextension=".txt",
            filetypes=(("TXT", "*.txt"), ("All Files", "*.*"))
        )
        if file:
            self.path[0] = file  # file path [0] --> original, [1] --> converted
            self.check_file_fn()  # prepare suitable file option

    def check_file_fn(self, convert=False):
        # ** check if file exists or task already done **
        file = self.path[0]
        is_file = os.path.isfile(file)
        if is_file:
            file_name = os.path.splitext(os.path.basename(file))[0]
            file_name += "_text2table.txt"  # converted file name
            cwd = os.path.dirname(file)
            perhaps_done = os.path.join(cwd, file_name)
            is_done = os.path.isfile(perhaps_done)
            if not is_done and convert:
                new_file = perhaps_done
                self.path[1] = new_file
                self.convert2table_fn()
            # * suitable file options *
            elif is_done:
                self.systray.update(menu_options=self.trayAlready)  # github.com/MagTun/infi.systray/tree/develop/src
            else:
                self.systray.update(menu_options=self.trayConvert)

    def convert2table_fn(self):
        # ** organize text file data to table like structure **
        table_dix = {"?": []}  # all table lists
        metadata = {"?": {"name": "?", "len": 0}}  # every list information
        table_titles_ls = []  # user custom list names
        pos = 0
        entries = 0
        with open(self.path[0], 'r') as f:
            file = f.read() + " "
        for index in range(len(file)):  # remove lines, tabs and spaces, organize words in lists
            char = file[index]
            if char in ' \t\n':
                word = file[pos:index]
                if word not in ' \t\n':
                    if word[-1].isupper():
                        if word[-1] in table_dix.keys():
                            table_dix[word[-1]].append(word)
                            if metadata[word[-1]]["len"] < len(word):
                                metadata[word[-1]]["len"] = len(word)
                            entries += 1
                        else:
                            table_dix[word[-1]] = []
                            table_dix[word[-1]].append(word)
                            metadata[word[-1]] = {}
                            metadata[word[-1]]["name"] = word[-1]
                            metadata[word[-1]]["len"] = len(word)
                            entries += 1
                    elif word[0] == "]":  # check for custom list names, ex: "]Players" as "Players" for title
                        table_titles_ls.append(word[1:])
                    else:  # uncategorized words
                        table_dix["?"].append(word)
                        if metadata["?"]["len"] < len(word):
                            metadata["?"]["len"] = len(word)
                        entries += 1
                pos = index + 1
        table_titles_ls.sort()
        for dix in metadata:  # apply user list names
            for header in table_titles_ls:
                if metadata[dix]["name"][0] == header[0]:
                    metadata[dix]["name"] = header
                    if metadata[dix]["len"] < len(header):
                        metadata[dix]["len"] = len(header)
        max_title_entries = 0
        for ls in table_dix:  # search max list length
            dix = ls
            metadata[dix]["entries"] = len(table_dix[dix])
            if max_title_entries < metadata[dix]["entries"]:
                max_title_entries = metadata[dix]["entries"]
            if metadata[dix]["len"] < len("~ " + str(metadata[dix]["entries"]) + " ~"):
                metadata[dix]["len"] = len("~ " + str(metadata[dix]["entries"]) + " ~")
        table_titles = ''
        title_sum_entries = ''
        space_line = ''
        for ls in sorted(table_dix.keys()):  # draw table 'tiles'
            dix = ls
            calibre = metadata[dix]["len"] + 2
            if not len(metadata[dix]["name"]) % 2 and calibre % 2:  # even title, odd calibre
                calibre += 1
            elif len(metadata[dix]["name"]) % 2 and not calibre % 2:  # odd title, even calibre
                calibre += -1
            title = metadata[dix]["name"].center(calibre, "_")
            table_titles += "|" + title
            space_line += "|" + " " * len(title)
            title_sum_entries += "|" + str("~ " + str(metadata[dix]["entries"]) + " ~").center(calibre, " ")
        # print(f'\nAll Entries: {entries}\n\n')  # dbg
        towrite = f'\nAll Entries: {entries}\n\n'
        # print("," * (len(table_titles) + 1) + '\n')  # dbg
        towrite += "," * (len(table_titles) + 1) + '\n'
        # print(space_line + "|\n")  # dbg
        towrite += space_line + "|\n"
        # print(table_titles + "|")  # dbg
        towrite += table_titles + "|\n"
        # print(space_line + "|")  # dbg
        towrite += space_line + "|\n"
        # print(title_sum_entries + "|")  # dbg
        towrite += title_sum_entries + "|\n"
        # print(space_line + "|")  # dbg
        towrite += space_line + "|\n"
        loop = 0
        while loop < max_title_entries:  # insert words into the appropriate table tile
            table_row = ''
            for ls in sorted(table_dix.keys()):
                dix = ls
                calibre = metadata[dix]["len"] + 2
                if not len(metadata[dix]["name"]) % 2 and calibre % 2:
                    calibre += 1
                elif len(metadata[dix]["name"]) % 2 and not calibre % 2:
                    calibre += -1
                if loop < metadata[dix]["entries"]:
                    if ls != "?":
                        table_row += "|" + table_dix[ls][loop][:-1].center(calibre, " ")
                    else:
                        table_row += "|" + table_dix[ls][loop].center(calibre, " ")
                else:
                    table_row += "|" + " " * calibre
            table_row += "|\n"
            towrite += table_row
            # print(table_row, end='')  # dbg
            loop += 1
        # print(space_line + "|")  # dbg
        towrite += space_line + "|\n"
        # print('"' * (len(table_titles) + 1))  # dbg
        towrite += '"' * (len(table_titles) + 1)
        towrite += "\n\ngithub.com/fireltom/PySimple"
        with open(self.path[1], 'w') as f:
            f.write(towrite)

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** run app **
        self.systray.start()  # tray


def main():
    # ** Text2table instance **
    txt2table = Text2table()
    txt2table.run()  # start instance


if __name__ == '__main__':
    main()  # executed only from text2table.py
