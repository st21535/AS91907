"""
Mainfile
Pycode

"""

# Importing the 3 modules from other files
from ProgressTrackervers3 import ProgressTracker
from TaskAddervers3 import TaskManger
from StudyClockVers3 import StudyClock

from tkinter import *


class MainFile:
    def __init__(self):
        # Setting up the tkinter window
        self.root = Tk()
        self.root.title("Study Buddy")
        self.root.geometry("500x445")
        self.root.resizable(False, False)  # Stops users from resizing
        self.root.configure(bg="#ffffff")  # White Background

        # This is the frame that all the content will go into
        self.frame = Frame(self.root, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        # This is the bottom frame, for the NAV buttons
        self.button_frame = Frame(self.root, bg="#ffffff")
        self.button_frame.pack(side="bottom", pady=10)

        # Creating a list to store the buttons - easier to delete/add
        self.menu_buttons = []

        # Showing first screen and then running the tk loop
        self.show_main_menu()

        self.root.mainloop()

    # Clears everything in that certain frame. So can switch to different
    # tasks without overlapping
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    # Different buttons dependant on task - so to clear buttons when switching
    def clear_buttons(self):
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

    def create_buttons(self, buttons_list):
        # Clears any existing buttons
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

        # Creates new buttons from the button list. (text, function)
        for text, cmd in buttons_list:
            buttons = Button(
                self.button_frame, text=text, font="Arial 12", command=cmd
            )
            buttons.pack(side="left", padx=5)
            self.menu_buttons.append(buttons)

    # The Main menu
    def show_main_menu(self):
        self.clear_frame()  # Clear any frames before
        self.clear_buttons()  # Clear all the buttons

        # Main Heading
        Label(
            self.frame,
            text="Study Buddy",
            font=("Verdana", 28, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).pack(pady=(50, 30))

        # Description
        Label(
            self.frame,
            text="Here to keep you locked in!! >:)",
            font=("Verdana", 14),
            bg="#ffffff",
            fg="#555555",
            wraplength=400,
            justify="center",
        ).pack(pady=(0, 40))

        # Menu buttons styling
        button_styles = {
            "font": ("Verdana", 14, "bold"),
            "bg": "#a85776",
            "fg": "white",
            "activebackground": "#be4152",
            "activeforeground": "white",
            "bd": 0,
            "width": 20,
            "pady": 10,
        }

        # Main menu options in a list
        buttons = [
            ("Task Adder", self.to_TMFrame),
            ("Progress Tracker", self.to_PTFrame),
            ("Study Tracker", self.to_CLFrame),
        ]

        # Taking the title and the function, creating buttons using the styles
        for text, cmd in buttons:
            buttons = Button(self.frame, text=text, command=cmd, **button_styles)
            buttons.pack(pady=10)

    # To Task Manager (TaskAdder)
    def to_TMFrame(self):
        self.clear_frame()  # Clear pre-existing frames
        TaskManger(self.frame)  # Running the file

        # Main menu + progress tracker button list
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame),
        ]
        self.create_buttons(buttons)  # Passing the list to function

    # To Progress Tracker
    def to_PTFrame(self):
        self.clear_frame()  # Clear pre-existing frames
        ProgressTracker(self.frame)  # Running the file

        # Main menu + task manager + study clock button list
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Task Manager", self.to_TMFrame),
            ("Study Tracker", self.to_CLFrame),
            ("How to Use", self.PTinfo)
        ]
        self.create_buttons(buttons)  # Passing the list to function

    def PTinfo(self):
        img=Toplevel()
        img.title("Information")

        img.geometry("400x200")
        img.resizable(False, False)


        PTinfo = PhotoImage(file = "PTInfo2.png")
        label=Label(img,image=PTinfo)
        label.image=PTinfo
        label.pack(expand=True)
    
    def SCinfo(self):
        img=Toplevel()
        img.title("Information")

        img.geometry("400x290")
        img.resizable(False, False)


        SCinfo = PhotoImage(file = "SCInfo2.png")
        label=Label(img,image=SCinfo)
        label.image=SCinfo
        label.pack(expand=True)

    # To (study) clock function
    def to_CLFrame(self):
        self.clear_frame()  # Clears pre-existing frames
        StudyClock(self.frame)  # Runs the file

        # Main menu + progress tracker
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame),
            ("How to Use",self.SCinfo)
        ]
        self.create_buttons(buttons)  # Passes list to function


# Running the program
if __name__ == "__main__":
    MainFile()
