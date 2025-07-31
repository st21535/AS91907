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
        self.root.geometry("600x600")

        
        frame=Frame(self.container)
        frame.grid(row=0,column=0,padx=10,pady=10)
        
        frame.rowconfigure(list(range(3),weight=1))
        frame.columnconfigure(list(range(3),weight=1))

        #Title
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "Title",justify=CENTER)
        self.prj_name_label.grid(sticky="WE",row=0,columnspan=2)


        with open("tasks.json", "r") as f:
                self.tasks=json.load(f)
        

        self.sorted_order=sorted(self.tasks, key=lambda item: item["Level"])

        for i, task in enumerate(self.sorted_order):
            name_label = Label(self.root, text=task["Project Name"], font="Arial 12", )
            name_label.grid(row=i+4, column=0, padx=10, pady=2)
        
        upcoming_label=Label(frame,text="Upcoming Due Dates",font="Arial 12")
        upcoming_label.grid(row=7,column=3,pady=5,padx=5)       

        
        '''
        name_label=Label(frame,text=self.tasks,font="arial 12", justify=LEFT)
        name_label.grid(row=4,column=0,padx=10,pady=10)
        '''
        
    def run(self):
        self.root.mainloop()
app = ProgressTracker()
app.run()

