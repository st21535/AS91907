from taskmanger_w_Json import TaskManger
from ProgressTracker import ProgressTracker
from StudyClock import StudyClock
from tkinter import *

class MainFile:
    def __init__(self):
        # make the main window
        self.root = Tk()
        self.root.title("Study Buddy")          # title text in the window bar
        self.root.geometry("500x450")           # fixed window size
        self.root.resizable(False, False)       # stop user from resizing window
        

        # main frame in the middle where different screens will load
        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # frame at the bottom just for nav buttons
        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="bottom", pady=10)

        # store the nav buttons here so we can update/clear them
        self.menu_buttons = []

        # start off by showing the main menu page
        self.show_main_menu()

        # run the app loop
        self.root.mainloop()

    # functions to manage the frames/buttons
    def clear_frame(self):
        # delete all widgets inside the main frame
        for widget in self.frame.winfo_children():
            widget.destroy()

    def clear_buttons(self):
        # delete all the buttons at the bottom
        for btn in self.menu_buttons:
            btn.destroy()
        self.menu_buttons = []

    def create_buttons(self, buttons_list):
        """buttons_list is a list like: [(label, command), ...]"""
        # remove old buttons first
        for btn in self.menu_buttons:
            btn.destroy()
        self.menu_buttons = []

        # create new buttons and place them side by side
        for text, cmd in buttons_list:
            btn = Button(self.button_frame, text=text, font="Arial 12", command=cmd)
            btn.pack(side="left", padx=5)
            self.menu_buttons.append(btn)


    # different pages
    def show_main_menu(self):
        self.clear_frame()
        Label(self.frame, text="Main Menu", font="Arial 20").pack(pady=50)
        # bottom buttons to go to each page
        buttons = [
            ("Task Manager", self.to_TMFrame),
            ("Progress Tracker", self.to_PTFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        self.create_buttons(buttons)

    def to_TMFrame(self):
        # switch to Task Manager screen
        self.clear_frame()
        TaskManger(self.frame)
        # bottom buttons for this screen
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

    def to_PTFrame(self):
        # switch to Progress Tracker screen
        self.clear_frame()
        ProgressTracker(self.frame)
        # bottom buttons for this screen
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Task Manager", self.to_TMFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        self.create_buttons(buttons)

    def to_CLFrame(self):
        # switch to Study Clock screen
        self.clear_frame()
        StudyClock(self.frame)
        # bottom buttons for this screen
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

if __name__ == "__main__":
    MainFile()