from tkinter import *
from tkinter import ttk, messagebox
import json
from datetime import datetime


class ProgressTracker:
    def __init__(self, parent):
        self.frame = Frame(parent, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        # Center container
        self.center_frame = Frame(self.frame, bg="#ffffff", padx=20, pady=20)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center") 

        # Load tasks
        self.tasks = self.load_tasks()

        # Frames for tasks and due dates inside center_frame
        self.left_frame = LabelFrame(self.center_frame, text="Tasks by Priority", padx=15, pady=15, bg="#ffffff", fg="#333333", font=("verdana",12,"bold"))
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.right_frame = LabelFrame(self.center_frame, text="Upcoming Due Dates", padx=15, pady=15, bg="#ffffff", fg="#333333", font=("verdana",12,"bold"))
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Make left/right frames expand evenly in center_frame
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=1)

        # Progress bar below frames
        self.progress_var = DoubleVar()
        style = ttk.Style()
        style.configure("green.Horizontal.TProgressbar", troughcolor='#e0e0e0', background='#4CAF50', thickness=20)

        self.progress_bar = ttk.Progressbar(self.center_frame, length=300, variable=self.progress_var, style="green.Horizontal.TProgressbar")
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=(10,0))
        
        self.progress_label = Label(self.center_frame, text="0%", font=("Verdana",12), bg="#ffffff", fg="#333333")
        self.progress_label.grid(row=2, column=0, columnspan=2, pady=(0,10))

        # Show tasks
        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()



    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                content = f.read().strip()
                if content != "":
                    return json.loads(content)
        except:
            pass
        return []

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    def show_priority_tasks(self):
        # Clear previous widgets
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Sort tasks by priority level
        sorted_tasks = []
        for task in self.tasks:
            sorted_tasks.append(task)
        sorted_tasks.sort(key=lambda x: int(x["Level"]))

        row_index = 0
        for task in sorted_tasks:
            done_var = IntVar()
            if task["Progress"] >= 100:
                done_var.set(1)
            else:
                done_var.set(0)

            completionbox_text = task["Project Name"] + " (P" + str(task["Level"]) + ")"
            completionbox = Checkbutton(self.left_frame, text=completionbox_text, variable=done_var,bg="#ffffff")
            completionbox.grid(row=row_index, column=0, sticky="w")

            # Add entry for progress
            progress_entry = Entry(self.left_frame, width=5)
            progress_entry.insert(0, str(task["Progress"]))
            progress_entry.grid(row=row_index, column=1)

            # Bind events
            def make_cb_command(t=task, v=done_var):
                return lambda: self.mark_complete(t, v)
            completionbox.config(command=make_cb_command())

            def make_entry_bind(t=task, e=progress_entry):
                return lambda event: self.update_progress(t, e)
            progress_entry.bind("<FocusOut>", make_entry_bind())

            row_index += 1

    def show_due_dates(self):
        # Clear previous widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        todays_date = datetime.today().date()

        # Sort tasks by due date
        sorted_tasks = []
        for task in self.tasks:
            sorted_tasks.append(task)
        sorted_tasks.sort(key=lambda x: datetime.strptime(x["Due Date"], "%d-%m-%Y"))

        for task in sorted_tasks:
            due_date = datetime.strptime(task["Due Date"], "%d-%m-%Y").date()
            prj_label = Label(self.right_frame, text=task["Project Name"] + " : " + task["Due Date"],bg='#ffffff',fg="#333333")
            prj_label.pack(anchor="w")

            if task["Progress"] < 100 and due_date < todays_date:
                messagebox.showwarning("Overdue Task!", task["Project Name"] + " was due on " + task["Due Date"] + "!")

    def mark_complete(self, task, var):
        if var.get() == 1:
            task["Progress"] = 100
            new_tasks = []
            for task in self.tasks:
                if task["Project Name"] != task["Project Name"]:
                    new_tasks.append(task)
            self.tasks = new_tasks
            self.save_tasks()
            self.show_priority_tasks()
            self.show_due_dates()
            self.update_progress_bar()

    def update_progress(self, task, entry):
        try:
            userinput = int(entry.get())
            if userinput < 0 or userinput > 100:
                raise ValueError
        except:
            messagebox.showerror("Invalid input", "Enter a number between 0 and 100")
            entry.delete(0, END)
            entry.insert(0, str(task["Progress"]))
            return

        task["Progress"] = userinput
        if userinput >= 100:
            new_tasks = []
            for task in self.tasks:
                if task["Project Name"] != task["Project Name"]:
                    new_tasks.append(task)
            self.tasks = new_tasks

        self.save_tasks()
        self.show_priority_tasks()
        self.show_due_dates()
        self.update_progress_bar()

    def update_progress_bar(self):
        if len(self.tasks) == 0:
            self.progress_var.set(0)
            self.progress_label.config(text="0/0")
            return

        total = 0
        for task in self.tasks:
            total += task["Progress"]
        avg = total / len(self.tasks)
        self.progress_var.set(avg)
        self.progress_label.config(text=str(int(avg)) + "%")

if __name__ == "__main__":
    root = Tk()
    app = ProgressTracker(root)
    root.mainloop()