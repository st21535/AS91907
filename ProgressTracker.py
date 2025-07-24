''''
Progress Tracker

'''


from tkinter import * 
import json
class ProgressTracker:
    def __init__(self):
        self.root=Tk()
        self.container=Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nesw")
        
        frame=Frame(self.container)
        #Main Heading````
        self.title_label=Label(frame,font="arial 16", text="Progress Tracker!")

        self.title_label.grid(row=0,columnspan=3,padx=10,pady=10)

        #getting name for project
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "Progress Tracker")
        self.prj_name_label.grid(sticky = NSEW)
        
    def run(self):
        self.root.mainloop()
app = ProgressTracker()
app.run()