from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
import json
from datetime import date


class TaskManger:
    def __init__(self, parent):
        self.frame = Frame(parent, bg="#f0f2f5")
        self.frame.pack(fill="both", expand=True)

        # Center container
        self.center_frame = Frame(self.frame, bg="#ffffff", padx=25, pady=25)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Heading
        Label(
            self.center_frame,
            text="Add Task",
            font=("Verdana", 18, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=(0, 15))

        # Project Name
        Label(
            self.center_frame,
            text="Project Name",
            font=("Verdana", 13),
            bg="#ffffff",
            fg="#555555"
        ).pack(anchor="w", pady=(5, 0))
        self.prj_name = Entry(
            self.center_frame,
            font=("Verdana", 12),
            justify=CENTER,
            bd=0,
            highlightthickness=1,
            highlightcolor="#a0a0a0",
            highlightbackground="#d0d0d0"
        )
        self.prj_name.pack(fill="x", pady=5, ipady=5)

        # Priority
        Label(
            self.center_frame,
            text="Priority Level",
            font=("Verdana", 13),
            bg="#ffffff",
            fg="#555555"
        ).pack(anchor="w", pady=(10, 0))
        self.levels = ["1", "2", "3", "4", "5"]
        self.radio_var = IntVar(value=-1)
        radio_frame = Frame(self.center_frame, bg="#ffffff")
        radio_frame.pack(pady=5)

        for i, lvl in enumerate(self.levels):
            radiobuttons = Radiobutton(
                radio_frame,
                text=lvl,
                variable=self.radio_var,
                value=i,
                font=("Verdana", 12),
                bg="#ffffff",
                activebackground="#ffffff",
                highlightthickness=0
            )
            radiobuttons.pack(side="left", padx=10)

        # Due Date
        Label(
            self.center_frame,
            text="Due Date",
            font=("Verdana", 13),
            bg="#ffffff",
            fg="#555555"
        ).pack(anchor="w", pady=(10, 0))
        self.due = DateEntry(
            self.center_frame,
            width=15,
            font=("Verdana", 12),
            mindate=date.today(),
            background="#ffffff",
            foreground="#333333",
            borderwidth=1
        )
        self.due.pack(pady=5)

        # Submit Button
        self.done_btn = Button(
            self.center_frame,
            text="Submit",
            font=("Verdana", 13),
            bg="#4CAF50",
            fg="#ffffff",
            bd=0
        )
        self.done_btn.pack(pady=15, ipadx=10, ipady=5, fill="x")
        self.done_btn.config(command=self.submit)

        # Status label
        self.status_label = Label(
            self.center_frame,
            text="",
            font=("Verdana", 12),
            bg="#ffffff",
            fg="#28a745"
        )
        self.status_label.pack(pady=(0, 5))

    def submit(self):
        # Ensuring only a valid date is inputed
        try:
            due_date = self.due.get_date().strftime("%d-%m-%Y")
        except Exception:
            messagebox.showerror("Invalid Date", "Please enter a valid date")
            return

        # no Empty name
        name = self.prj_name.get().strip()
        if not name:
            messagebox.showerror("Missing Data", "Project name cannot be empty")
            return

        # Making sure there are no name dupes
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = []

        if type(data) != list:
            data = []

        for task in data:
            if isinstance(task, dict) and "Project Name" in task:
                if task["Project Name"].lower() == name.lower():
                    messagebox.showerror("Duplicate", f"'{name}' already exists")
                    return

        # Need to select a priorty level
        if self.radio_var.get() == -1:
            messagebox.showerror("Missing Data", "Please select a priority level (1-5)")
            return

        # appending to json
        info = {
            "Project Name": name,
            "Level": str(self.levels[self.radio_var.get()]) if self.radio_var.get() != -1 else "0",
            "Due Date": due_date,
            "Progress": 0
        }

        data.append(info)
        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)

        # Reseting the inputs
        self.prj_name.delete(0, END)
        self.radio_var.set(-1)
        self.due.set_date(date.today())
        self.status_label.config(text="Task Added ")
