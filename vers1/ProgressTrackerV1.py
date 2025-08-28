from tkinter import *
from tkinter import ttk
import json
from datetime import datetime

class ProgressTracker:
    def __init__(self,parent):
        # create a main frame inside the parent window
        self.frame=Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")  
        self.root = parent   # reference to parent window

        # load tasks from file
        self.tasks = self.load_tasks()

        # set up the GUI layout (left/right frames + progress bar)
        self.setup_layout()

        # populate the frames
        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()

    def setup_layout(self):
        # configure root grid layout so frames scale nicely
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # left frame: shows tasks ordered by priority
        self.left_frame = LabelFrame(self.frame, text="Tasks by Priority", padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # right frame: shows upcoming due dates
        self.right_frame = LabelFrame(self.frame, text="Upcoming Due Dates", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # progress bar at the bottom of the window
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    # file handling
    def load_tasks(self):
        # load JSON tasks file, return empty list if file missing or empty
        try:
            with open("tasksv1.json", "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except:
            pass
        return []

    def save_tasks(self):
        # save tasks list to JSON file
        with open("tasksv1.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    # GUI display updates
    def show_priority_tasks(self):
        # clear the left frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # sort tasks by "Level" (priority)
        sorted_tasks = sorted(self.tasks, key=lambda task: int(task["Level"]))

        row_number = 0
        for task in sorted_tasks:
            # checkbox variable (checked if progress = 100)
            done_var = IntVar(value=1 if task["Progress"] == 100 else 0)

            # checkbox text shows task name + priority
            cb_text = f"{task['Project Name']} (P{task['Level']})"
            cb = Checkbutton(self.left_frame, text=cb_text, variable=done_var,
                             command=lambda t=task, v=done_var: self.mark_complete(t, v))
            cb.grid(row=row_number, column=0, sticky="w")

            # entry box to update progress manually
            entry = Entry(self.left_frame, width=5)
            entry.insert(0, task["Progress"])
            entry.grid(row=row_number, column=1)

            # update progress when focus leaves entry
            entry.bind("<FocusOut>", lambda e, t=task, ent=entry: self.update_progress(t, ent))
            row_number += 1

    def show_due_dates(self):
        # clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # sort tasks by due date
        sorted_tasks = sorted(self.tasks, key=lambda task: datetime.strptime(task["Due Date"], "%Y-%m-%d"))

        # show each task and its due date
        for task in sorted_tasks:
            Label(self.right_frame, text=f"{task['Project Name']} - {task['Due Date']}").pack(anchor="w")

    # user inputs
    def mark_complete(self, task, var):
        # mark a task as complete when checkbox clicked
        if var.get() == 1:
            task["Progress"] = 100
            # remove task from the list after completed
            self.tasks = [t for t in self.tasks if t["Project Name"] != task["Project Name"]]
            self.save_tasks()
            # refresh GUI
            self.show_priority_tasks()
            self.show_due_dates()
            self.update_progress_bar()

    def update_progress(self, task, entry):
        # update task progress when entry edited
        try:
            new_value = int(entry.get())
        except ValueError:
            return
        
        task["Progress"] = new_value
        # remove if progress is 100
        if new_value >= 100:
            self.tasks = [t for t in self.tasks if t["Project Name"] != task["Project Name"]]
        self.save_tasks()
        # refresh GUI
        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()

    # progress bar

    def update_progress_bar(self):
        # calculate average progress for all tasks
        if not self.tasks:
            self.progress_var.set(0)
            return
        avg = sum(task["Progress"] for task in self.tasks) / len(self.tasks)
        self.progress_var.set(avg)


if __name__ == "__main__":
    root = Tk()
    ProgressTracker(root)
    root.mainloop()
