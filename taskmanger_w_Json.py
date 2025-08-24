from tkinter import * 
from tkcalendar import DateEntry
from tkinter import messagebox
import json
from datetime import date

class TaskManger:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")  

        # Main Heading
        self.add_task_label = Label(self.frame, font="arial 16", text="Add Task!")
        self.add_task_label.grid(row=0, columnspan=3, padx=10, pady=10)

        # Project name
        self.prj_name_label = Label(self.frame, font="Arial 16", text="Name Of Project")
        self.prj_name_label.grid(sticky=NSEW)
        self.prj_name = Entry(self.frame, justify=CENTER)
        self.prj_name.grid(row=2)

        # Priority level
        self.levels = ["1", "2", "3", "4", "5"]
        self.radio_var = IntVar()
        self.radio_var.set(0)

        self.levels_label = Label(self.frame, font="Arial 16", text="Priority Level")
        self.levels_label.grid(sticky=NSEW, row=3)

        for i in range(5):
            Radiobutton(
                self.frame, font="Arial 11", text=self.levels[i],
                variable=self.radio_var, value=i
            ).grid(row=(i+4), column=0, sticky="nsew", columnspan=1, padx=60)

        # Due Date
        get_date_label = Label(self.frame, font="Arial 16", text="Due Date")
        get_date_label.grid(sticky=NSEW, row=11)

        self.due = DateEntry(self.frame, width=15, year=2025, month=7, date_pattern="dd-mm-yyyy",mindate=date.today() 
)
        self.due.grid(row=12)

        self.name_button = Button(self.frame, text="Submit", font="Arial 16", command=self.info)
        self.name_button.grid(padx=10, pady=10, row=13)

    def info(self):
        try:
            due_date_obj = self.due.get_date()
            due_date = due_date_obj.strftime("%d-%m-%Y")
        except Exception:
            messagebox.showerror("Invalid Date", "Please enter a valid date in d-m-y format.")
            return


        project_name = self.prj_name.get().strip()
        if not project_name:
            messagebox.showerror("Missing Data", "Project name cannot be empty.")
            return

        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        for task in data:
            if task["Project Name"].lower() == project_name.lower():
                messagebox.showerror("Duplicate Project", f"A project named '{project_name}' already exists.")
                return
        else:
            pass   

        info = {
            "Project Name": project_name,
            "Level": str(self.levels[self.radio_var.get()]),
            "Due Date": due_date,
            "Progress": 0
        }

        data.append(info)

        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)

        # Confirmation
        self.completed_label = Label(self.frame, font="arial 16", text="Task Added ✅")
        self.completed_label.grid(sticky=NSEW, row=16)

        self.prj_name.delete(0, END)
        self.radio_var.set(0)
        self.due.set_date(date.today())
