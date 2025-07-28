
from tkinter import * 
import json
class StudyClock:
    def __init__(self):
        self.root=Tk()
        self.root.title("StudyClock!")
        self.container=Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nesw")
        
        frame=Frame(self.container)
        frame.grid(row=0,column=0,padx=10,pady=10)
        #Title
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "StudyClock")
        self.prj_name_label.grid(sticky = NSEW,row=1)

        
    def run(self):
        self.root.mainloop()
app = StudyClock()
app.run()