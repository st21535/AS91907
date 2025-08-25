
'''
V2 Validation
'''
from taskmanger import TaskManger
from progresstracker import ProgressTracker
from StudyClock import StudyClock
from tkinter import *

class MainFile:
    def __init__(self):
        self.root = Tk()
        self.root.title("Study Buddy")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        

        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="bottom", pady=10)

        self.menu_buttons = []

        self.show_main_menu()

        self.root.mainloop()


    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def clear_buttons(self):
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

    def create_buttons(self, buttons_list):
        """buttons_list = [(label, command), ...]"""
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

        for text, cmd in buttons_list:
            buttons = Button(self.button_frame, text=text, font="Arial 12", command=cmd)
            buttons.pack(side="left", padx=5)
            self.menu_buttons.append(buttons)


    def show_main_menu(self):
        self.clear_frame()
        Label(self.frame, text="Main Menu", font="Arial 20").pack(pady=50)


        
        buttons = [
            ("Task Manager", self.to_TMFrame),
            ("Progress Tracker", self.to_PTFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        self.create_buttons(buttons)

    def to_TMFrame(self):
        self.clear_frame()
        TaskManger(self.frame)

        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

    def to_PTFrame(self):
        self.clear_frame()
        ProgressTracker(self.frame)

        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Task Manager", self.to_TMFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        self.create_buttons(buttons)

    def to_CLFrame(self):
        self.clear_frame()
        StudyClock(self.frame)

        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

if __name__ == "__main__":
    MainFile()