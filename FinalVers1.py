from taskmanger_w_Json import TaskManger
from ProgressTracker import ProgressTracker
from StudyClock import StudyClock
from tkinter import *

class MainFile:
    def __init__(self):
        self.root = Tk()
        self.root.title("Study Buddy")
        self.root.geometry("600x400")

        self.frame = Frame(self.root)
        self.frame.pack(fill="both", expand=True)


        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="bottom", fill="x", pady=10)


        self.to_TM_button = Button(self.button_frame, text="Task Manager", font="Arial 12 ", 
                                  command=self.to_TMFrame)
        self.to_TM_button.pack(side="left", padx=5)

        self.to_PT_button = Button(self.button_frame, text="Progress Tracker", font="Arial 12 ", 
                                  command=self.to_PTFrame)
        self.to_PT_button.pack(side="left", padx=5)

        self.to_SL_button = Button(self.button_frame, text="Study Tracker", font="Arial 12 ", 
                                  command=self.to_CLFrame)
        self.to_SL_button.pack(side="left", padx=5)



        self.root.mainloop()

    def to_TMFrame(self):
        self.clear_frame()
        TaskManger(self.frame)
    
    def to_PTFrame(self):
        self.clear_frame()
        ProgressTracker(self.frame)
    def to_CLFrame(self):
        self.clear_frame()
        StudyClock(self.frame)


    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()


if __name__=="__main__":
    MainFile()

    
    