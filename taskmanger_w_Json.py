from tkinter import * 
from tkcalendar import DateEntry
import json
from datetime import date

class TaskManger:
    def __init__(self):
        self.root=Tk()
        self.container=Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nesw")
        
        frame=Frame(self.container)
        #Main Heading
        self.add_task_label=Label(frame,font="arial 16", text="Add Task!")

        self.add_task_label.grid(row=0,columnspan=3,padx=10,pady=10)

        #getting name for project
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "Name Of Project")
        self.prj_name_label.grid(sticky = NSEW)

        self.prj_name = Entry(self.root, justify = CENTER)
        self.prj_name.grid(row=2)

        #getting Priorty Level
        self.levels = ["1", "2", "3", "4","5"]
        self.radio_var = IntVar()
        self.radio_var.set(99)

        self.levels_label = Label(self.root, font = "Arial 16", text = "Priorty Level")
        self.levels_label.grid(sticky = NSEW,row=3)

        for i in range(5):
            Radiobutton(self.root, font = "Arial 11",text=self.levels[i], variable=self.radio_var, value = i, ).grid(row = (i+4), column = 0, sticky="nsew", columnspan=1, padx=60)


        #Getting Date
        
        
        get_date_label=Label(self.root,font = "Arial 16", text = "Due Date" )
        get_date_label.grid(sticky = NSEW,row=11)

        due=DateEntry(self.root, width=15,year=2025,month=7)
        due.grid(row=12)

        #Submit Button
        self.name_button = Button(self.root, text="Submit", font="Arial 16",command=self.info)
        self.name_button.grid(padx=10,pady=10,row=13)
        
    def info(self):
        '''
        selected_date = self.cal.get_date()
        print(selected_date)
        self.name = str(self.levels[self.radio_var.get()]) + " " + str(self.prj_name.get() )

        self.name_label = Label(self.root, font = "Arial 16", text = self.name)
        self.name_label.grid(sticky = NSEW,row=14)
        '''
        info={"Project Name": str(self.prj_name.get()), "Level":str(self.levels[self.radio_var.get()]), "Due Date": str(self.due.get_date())}
        print(info)
        
        with open("tasks.json", "r") as f:
            json.dump(info, f, indent=4) 
            
        
        
    def run(self):
        self.root.mainloop()
app = TaskManger()
app.run()
'''
        entrybox

        oeuirty level-0radiobutton\duedate
        
        '''



