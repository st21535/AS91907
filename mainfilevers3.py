
from tkinter import *

class MainFile:
    def __init__(self):
        self.root = Tk()
        self.root.title("Study Buddy")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")


        
        self.frame = Frame(self.root,bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        
        self.button_frame = Frame(self.root,bg="#ffffff")
        self.button_frame.pack(side="bottom", pady=10)

        
        self.menu_buttons = []

        
        self.show_main_menu()

        self.root.mainloop()

        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)


        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")



    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def clear_buttons(self):
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

    def create_buttons(self, buttons_list):        
        for buttons in self.menu_buttons:
            buttons.destroy()
        self.menu_buttons = []

        
        for text, cmd in buttons_list:
            buttons = Button(self.button_frame, text=text, font="Arial 12", command=cmd)
            buttons.pack(side="left", padx=5)
            self.menu_buttons.append(buttons)


    def show_main_menu(self):
        self.clear_frame()
        #Main Heading
        Label(self.frame, text="Study Buddy", font=("Verdana", 28, "bold"), bg="#ffffff", fg="#333333").pack(pady=(50, 30))
        # description
        Label(self.frame,text="Here to keep you locked in!! >:)",font=("Verdana", 14),bg="#ffffff",fg="#555555",wraplength=400,justify="center").pack(pady=(0, 40))
        
        # Menu buttons
        button_styles = {"font": ("Verdana", 14, "bold"),
            "bg": "#a85776",
            "fg": "white",
            "activebackground": "#be4152",
            "activeforeground": "white",
            "bd": 0,
            "width": 20,
            "pady": 10
        }
        
        buttons = [
            ("Task Manager", self.to_TMFrame),
            ("Progress Tracker", self.to_PTFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        
        for text, cmd in buttons:
            buttons = Button(self.frame, text=text, command=cmd, **button_styles)
            buttons.pack(pady=10)


    def to_TMFrame(self):
        self.clear_frame()
        TaskManger(self.frame)
        #main menu + progress tracker
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

    def to_PTFrame(self):
        self.clear_frame()
        ProgressTracker(self.frame)
        #main menu + task manager + study clock
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Task Manager", self.to_TMFrame),
            ("Study Tracker", self.to_CLFrame)
        ]
        self.create_buttons(buttons)

    def to_CLFrame(self):
        self.clear_frame()
        StudyClock(self.frame)
        #main menu + progress tracker
        buttons = [
            ("Main Menu", self.show_main_menu),
            ("Progress Tracker", self.to_PTFrame)
        ]
        self.create_buttons(buttons)

if __name__ == "__main__":
    MainFile()