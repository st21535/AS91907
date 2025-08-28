
'''
v1
'''
from tkinter import * 
from tkcalendar import DateEntry
import json
from datetime import date

class TaskManger:
    def __init__(self,parent):
        # create main frame inside the parent
        self.frame=Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")  

        # Main heading
        self.add_task_label=Label(self.frame,font="arial 16", text="Add Task!")
        self.add_task_label.grid(row=0,columnspan=3,padx=10,pady=10)

        # Project name input
        self.prj_name_label = Label(self.frame, font = "Arial 16", text = "Name Of Project")
        self.prj_name_label.grid(sticky = NSEW)

        self.prj_name = Entry(self.frame, justify = CENTER)
        self.prj_name.grid(row=2)

        # Priority level (radio buttons)
        self.levels = ["1", "2", "3", "4","5"]
        self.radio_var = IntVar()
        self.radio_var.set(0)   # default selected = 0

        self.levels_label = Label(self.frame, font = "Arial 16", text = "Priorty Level")
        self.levels_label.grid(sticky = NSEW,row=3)

        # create radio buttons for priority levels
        for i in range(5):
            Radiobutton(
                self.frame,
                font = "Arial 11",
                text=self.levels[i],
                variable=self.radio_var,
                value = i,
            ).grid(row = (i+4), column = 0, sticky="nsew", columnspan=1, padx=60)
        get_date_label=Label(self.frame,font = "Arial 16", text = "Due Date" )
        get_date_label.grid(sticky = NSEW,row=11)

        # Date picker widget
        self.due=DateEntry(self.frame, width=15,year=2025,month=7)
        self.due.grid(row=12)

        # Submit button
        self.name_button = Button(self.frame, text="Submit", font="Arial 16",command=self.info)
        self.name_button.grid(padx=10,pady=10,row=13)
        
    #saveing task info
    def info(self):
        # collect info from the user inputs
        info={
            "Project Name": str(self.prj_name.get()), 
            "Level":str(self.levels[self.radio_var.get()]), 
            "Due Date": str(self.due.get_date()),
            "Progress":0
        }
        print(info)  # print to console for testing

        # load existing tasks if file exists, otherwise start empty
        try:
            with open("tasksv1.json", "r") as f:
                data=json.load(f)
        except:
            data=[]
        
        # add new task
        data.append(info)
    
        # save updated tasks back to file
        with open("tasksv1.json", "w") as f:
            json.dump(data, f, indent=4) 

        # display confirmation to user
        self.completed_label=Label(self.frame,font="arial 16",text="Task Added")
        self.completed_label.grid(sticky = NSEW,row=16)


if __name__ == "__main__":
    root = Tk()
    TaskManger(root)
    root.mainloop()
