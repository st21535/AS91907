''''
Progress Tracker

'''

from tkinter import * 
import json
class ProgressTracker:
    def __init__(self):
        self.root=Tk()
        self.root.title("Progress Tracker!")
        self.container=Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nesw")
        
        frame=Frame(self.container)
        frame.grid(row=0,column=0,padx=10,pady=10)
        #Title
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "Progress Tracker")
        self.prj_name_label.grid(sticky = NSEW,row=1)
        


        with open("tasks.json", "r") as f:
                self.tasks=json.load(f)
        
        self.tests=self.tasks[1]
        print(self.tests["Project Name"])

        for i, task in enumerate(self.tasks):
            name_label = Label(frame, text=task["Project Name"], font="Arial 12", anchor="w", justify=LEFT)
            name_label.grid(row=i+2, column=0, sticky=W, padx=10, pady=2)
        
        '''
        name_label=Label(frame,text=self.tasks,font="arial 12", justify=LEFT)
        name_label.grid(row=4,column=0,padx=10,pady=10)
        '''
        
    def run(self):
        self.root.mainloop()
app = ProgressTracker()
app.run()

