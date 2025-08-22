from taskmanger_w_Json import TaskManger
from ProgressTracker import ProgressTracker
from StudyClock import StudyClock
from tkinter import *

class MainFile:
    def __init__(self):
        if __name__=="__main__":
            self.root = Tk()
            self.root.title("Study Buddy")
            self.root.geometry("600x400")

        self.to_TM_button = Button(self.root, text="Task Manager", font="Arial 12 ", 
                                  command=self.to_TMFrame)
        self.to_TM_button.grid(row=1, column=0, padx=10, pady=10)

        self.to_PT_button = Button(self.root, text="Progress Tracker", font="Arial 12 ", 
                                  command=self.to_PTFrame)
        self.to_PT_button.grid(row=1, column=2, padx=10, pady=10)

        self.to_SL_button = Button(self.root, text="Study Tracker", font="Arial 12 ", 
                                  command=self.to_CLFrame)
        self.to_SL_button.grid(row=1, column=3, padx=10, pady=10)

        self.frame=Frame(self.root)
        self.frame.grid(row=1,column=1,columnspan=2)

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



    def run(self):
        self.root.mainloop()

MainFile().run()
    