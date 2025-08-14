from tkinter import *
from tkinter import ttk
import json
from datetime import datetime

class ProgressTracker:
    def __init__(self):
        self.root = Tk()
        self.root.title("Progress Tracker")
        self.root.geometry("600x400")

        self.tasks = self.load_tasks()

        self.setup_layout()

        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()

    def setup_layout(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.left_frame = LabelFrame(self.root, text="Tasks by Priority", padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = LabelFrame(self.root, text="Upcoming Due Dates", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except:
            pass
        return []

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    def show_priority_tasks(self):

        sorted_tasks = sorted(self.tasks, key=lambda task: int(task["Level"]))

        row_number = 0
        for task in sorted_tasks:
            done_var = IntVar(value=1 if task["Progress"] == 100 else 0)

            cb_text = f"{task['Project Name']} (P{task['Level']})"
            cb = Checkbutton(self.left_frame, text=cb_text, variable=done_var,
                             command=lambda t=task, v=done_var: self.mark_complete(t, v))
            cb.grid(row=row_number, column=0, sticky="w")

            entry = Entry(self.left_frame, width=5)
            entry.insert(0, task["Progress"])
            entry.grid(row=row_number, column=1)

            entry.bind("<FocusOut>", lambda e, t=task, ent=entry: self.update_progress(t, ent))
            row_number += 1

    def show_due_dates(self):

        sorted_tasks = sorted(self.tasks, key=lambda task: datetime.strptime(task["Due Date"], "%Y-%m-%d"))

        for task in sorted_tasks:
            Label(self.right_frame, text=f"{task['Project Name']} - {task['Due Date']}").pack(anchor="w")


    def mark_complete(self, task, var):
        if var.get() == 1:
            task["Progress"] = 100
            self.tasks = [t for t in self.tasks if t["Project Name"] != task["Project Name"]]
            self.save_tasks()
            self.show_priority_tasks()
            self.show_due_dates()
            self.update_progress_bar()

    def update_progress(self, task, entry):
        new_value = int(entry.get())  
        task["Progress"] = new_value
        if new_value >= 100:
            self.tasks = [t for t in self.tasks if t["Project Name"] != task["Project Name"]]
        self.save_tasks()
        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()

    def update_progress_bar(self):
        if not self.tasks:
            self.progress_var.set(0)
            return
        avg = sum(task["Progress"] for task in self.tasks) / len(self.tasks)
        self.progress_var.set(avg)

    def run(self):
        self.root.mainloop()

app = ProgressTracker()
app.run()