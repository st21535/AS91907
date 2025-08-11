'''
Version 1 With all Features

'''


from tkinter import *
import json
from datetime import datetime
from tkcalendar import DateEntry

class StudyClock:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x400")
        self.root.title("Study Buddy")

        self.container = Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nswe")


        self.frames = {}

        self.frames["MainFrame"] = self.create_main_frame()
        self.frames["AddTask"] = self.create_to_addtask()
        self.frames["Tracker"] = self.create_to_tracker()
        self.frames["StudyClock"] = self.create_to_clock()
        
        self.show_frame("MainFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        
    def create_main_frame(self):
        frame = Frame(self.container)

        self.main_title_label=Label(frame,font="Arial 16", text="Study Buddy!")
        self.main_title_label.grid(row=0,columnspan=3,padx=10,pady=10)

        self.to_task_button=Button(frame, text="To Tracker",font="Arial 12",command=lambda:self.show_frame("Tracker"))
        self.to_task_button.grid(row=1,column=0,padx=10,pady=10)

        self.to_task_button=Button(frame, text="To task adder",font="Arial 12",command=lambda:self.show_frame("AddTask"))
        self.to_task_button.grid(row=1,column=1,padx=10,pady=10)

        self.to_task_button=Button(frame, text="StudyClock",font="Arial 12",command=lambda:self.show_frame("StudyClock"))
        self.to_task_button.grid(row=1,column=2,padx=10,pady=10)
        frame.grid(row=0, column=0, sticky="nswe")
        return frame

    def create_to_addtask(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")

        
        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame
    def create_to_tracker(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)
        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame
    def create_to_clock(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)

        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame

    def run(self):
        self.root.mainloop()

StudyClock().run()
class TaskManger:
    def __init__(self):
        self.root=Tk()
        self.root.geometry("600x400")
        self.container=Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nesw")
        self.root.grid_rowconfigure(0, weight=1)   
        self.root.grid_rowconfigure(1, weight=0)   
        self.root.grid_columnconfigure(1, weight=1) 
        self.root.grid_columnconfigure(0,weight=1)

        #Main Headin
        self.add_task_label=Label(self.root,font="arial 16", text="Add Task!")
        self.add_task_label.grid(columnspan=2,row=0)

        #Title
        self.prj_name_label = Label(self.root, font = "Arial 16", text = "Name Of Project")
        self.prj_name_label.grid(columnspan=2,row=1)
        #Getting Name For Project
        self.prj_name = Entry(self.root, justify = CENTER)
        self.prj_name.grid(row=2,columnspan=2)

        #getting Priorty Level
        self.levels = ["1", "2", "3", "4","5"]
        self.radio_var = IntVar()
        self.radio_var.set(99)

        self.levels_label = Label(self.root, font = "Arial 16", text = "Priorty Level")
        self.levels_label.grid(columnspan=2,row=3)

        for i in range(5):
            Radiobutton(self.root, font = "Arial 11",text=self.levels[i], variable=self.radio_var, value = i, ).grid(row = (i+4), column = 0, sticky="nsew", columnspan=2, padx=60)

        #Getting Date
        
        get_date_label=Label(self.root,font = "Arial 16", text = "Due Date" )
        get_date_label.grid(columnspan=2,row=11)

        self.due=DateEntry(self.root, width=15,year=2025,month=7)
        self.due.grid(row=12,columnspan=2)

        #Submit Button
        self.name_button = Button(self.root, text="Submit", font="Arial 16",command=self.info)
        self.name_button.grid(padx=10,pady=10,row=13,columnspan=2)
        
    def info(self):

        info={"Project Name": str(self.prj_name.get()), "Level":str(self.levels[self.radio_var.get()]), "Due Date": str(self.due.get_date()),"Progress":0}
        print(info)
        try:
            with open("tasks.json", "r") as f:
                data=json.load(f)
        except:
            data=[]
        data.append(info)
    
        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4) 
        
    def run(self):
        self.root.mainloop()

class ProgressTracker:
    def __init__(self):
        self.root = Tk()
        self.root.title("Progress Tracker")
        self.root.geometry("600x400")

        self.tasks = self.load_tasks()

        self.root.grid_rowconfigure(0, weight=1)   
        self.root.grid_rowconfigure(1, weight=0)   
        self.root.grid_columnconfigure(1, weight=1) 
        self.root.grid_columnconfigure(0,weight=1)

        self.left_frame = LabelFrame(self.root, text="Tasks by Priority", padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = LabelFrame(self.root, text="Upcoming Due Dates", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


        self.display_left_panel()
        self.display_right_panel()

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                tasks = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []
        return tasks

    def display_left_panel(self):

        self.sorted_order=sorted(self.tasks, key=lambda item: item["Level"])

        for i, task in enumerate(self.sorted_order):

            checkbox_progress = Checkbutton(self.left_frame, text=f"{task['Project Name']}")
            checkbox_progress.grid(row=i, column=0, sticky="w")

            entry = Entry(self.left_frame, width=5)
            entry.insert(0, task["Progress"])
            entry.grid(row=i, column=1)

    def display_right_panel(self):
        sorted_tasks = sorted(self.tasks, key=lambda item: datetime.strptime(item["Due Date"], "%Y-%m-%d"))

        for task in sorted_tasks:
            Label(self.right_frame, text=f"{task['Project Name']} : {task['Due Date']}").grid(sticky="nsew")
       
    def run(self):
        self.root.mainloop()

app = StudyClock()
app.run()
