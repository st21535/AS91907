from tkinter import *
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ProgressTracker:
    def __init__(self, parent):
        self.root = parent
 
        self.tasks = self.load_tasks()

        # Frames
        self.left_frame = LabelFrame(self.root, text="Tasks by Priority")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        self.right_frame = LabelFrame(self.root, text="Upcoming Due Dates")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        # Progress bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=10)
        self.progress_label = Label(self.root, text="0%")
        self.progress_label.grid(row=2, column=0, columnspan=2)

        # Buttons to update progress
        btn_complete = Button(self.root, text="Mark Completed Tasks", command=self.mark_all_complete)
        btn_complete.grid(row=3, column=0, pady=5)
        btn_update = Button(self.root, text="Update Progress", command=self.update_all_progress)
        btn_update.grid(row=3, column=1, pady=5)

        self.show_tasks()
        self.update_progress_bar()

    # ----------------------- Load / Save -----------------------
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                return json.load(f)
        except:
            return []

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    # ----------------------- Display Tasks -----------------------
    def show_tasks(self):
        # Clear frames
        for w in self.left_frame.winfo_children():
            w.destroy()
        for w in self.right_frame.winfo_children():
            w.destroy()

        today = datetime.today().date()

        # Sort by priority for left frame
        for i, task in enumerate(sorted(self.tasks, key=lambda t: int(t["Level"]))):
            # Checkbox variable
            task["done_var"] = IntVar(value=1 if task["Progress"] >= 100 else 0)
            cb = Checkbutton(self.left_frame, text=f"{task['Project Name']} (P{task['Level']})", variable=task["done_var"])
            cb.grid(row=i, column=0, sticky="w")

            # Progress entry
            task["entry"] = Entry(self.left_frame, width=5)
            task["entry"].insert(0, str(task["Progress"]))
            task["entry"].grid(row=i, column=1)

        # Right frame: due dates
        for task in sorted(self.tasks, key=lambda t: datetime.strptime(t["Due Date"], "%d-%m-%Y")):
            lbl = Label(self.right_frame, text=f"{task['Project Name']} - {task['Due Date']}")
            lbl.pack(anchor="w")
            due_date = datetime.strptime(task["Due Date"], "%d-%m-%Y").date()
            if task["Progress"] < 100 and due_date < today:
                messagebox.showwarning("Overdue Task!", f"{task['Project Name']} was due on {task['Due Date']}!")

    # ----------------------- Update Functions -----------------------
    def mark_all_complete(self):
        for task in self.tasks:
            if task["done_var"].get() == 1:
                task["Progress"] = 100
        self.save_tasks()
        self.show_tasks()
        self.update_progress_bar()

    def update_all_progress(self):
        for task in self.tasks:
            try:
                val = int(task["entry"].get())
                if val < 0 or val > 100:
                    raise ValueError
            except:
                task["entry"].delete(0, END)
                task["entry"].insert(0, str(task["Progress"]))
                continue
            task["Progress"] = val
        self.save_tasks()
        self.show_tasks()
        self.update_progress_bar()

    # ----------------------- Progress Bar -----------------------
    def update_progress_bar(self):
        if not self.tasks:
            self.progress_var.set(0)
            self.progress_label.config(text="0%")
            return
        avg = sum(t["Progress"] for t in self.tasks) / len(self.tasks)
        self.progress_var.set(avg)
        self.progress_label.config(text=f"{int(avg)}%")

# ----------------------- Run App -----------------------
if __name__ == "__main__":
    root = Tk()
    app = ProgressTracker(root)
    root.mainloop()
