'''
Progress tracking

Vers1
-Ordered tasks by priorty + due date 
-Need Progress bar
'''

from tkinter import *

import json
from datetime import datetime

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

        self.bottom_frame = LabelFrame(self.root, text="Progress Bar", padx=10, pady=10)
        self.bottom_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.display_left_panel()
        self.display_right_panel()
        self.display_progress_bar()

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

            checkbox_progress = Checkbutton(self.left_frame, text=f"{task['Project Name']}",command=self.update_progress)
            checkbox_progress.grid(row=i, column=0, sticky="w")




            entry = Entry(self.left_frame, width=5)
            entry.insert(0, task["Progress"])
            entry.grid(row=i, column=1)

    def display_right_panel(self):
        sorted_tasks = sorted(self.tasks, key=lambda item: datetime.strptime(item["Due Date"], "%Y-%m-%d"))

        for task in sorted_tasks:
            Label(self.right_frame, text=f"{task['Project Name']} : {task['Due Date']}").grid(sticky="nsew")
    def update_progress(self):  
        #1==not checked
        #0==Checked
        num=self.checkbox_progress.get()
        if num==1:
            print("hello")
        else:
            print("goodbye")
    def display_progress_bar(self):
        pass
       
    def run(self):
        self.root.mainloop()
app = ProgressTracker()
app.run()