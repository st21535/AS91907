import time
import threading
from tkinter import *
from tkinter import ttk, messagebox
import json

class StudyClock:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")


        self.tasks = []
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []

        task_names = []
        for t in self.tasks:
            task_names.append(t["Project Name"])

        if not task_names:
            task_names = ["no tasks"]

        self.selected_task = StringVar()
        self.selected_task.set(task_names[0])

        self.task_label = Label(self.frame, text="Select Task:", font=("Arial", 12))
        self.task_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.task_menu = ttk.Combobox(self.frame, textvariable=self.selected_task, values=task_names, state="readonly")
        self.task_menu.grid(row=0, column=1, padx=10, pady=5)

        self.cycles_label = Label(self.frame, text="How many cycles (max 5):", font=("Arial", 12))
        self.cycles_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.cycle_entry = Entry(self.frame)
        self.cycle_entry.insert(0, "1")
        self.cycle_entry.grid(row=1, column=1, padx=10, pady=5)

        self.timer_display = Label(self.frame, text="00:00", font=("Arial", 20))
        self.timer_display.grid(row=2, column=0, columnspan=2, pady=10)


        self.start_btn = Button(self.frame, text="Start", width=10, command=self.start_timer)
        self.start_btn.grid(row=3, column=0, pady=5)
        self.stop_btn = Button(self.frame, text="Stop", width=10, command=self.stop_timer)
        self.stop_btn.grid(row=3, column=1, pady=5)


        self.progress = ttk.Progressbar(self.frame, length=200)
        self.progress.grid(row=4, column=0, columnspan=2, pady=10)
        self.progress_label = Label(self.frame, text="0/0 cycles done")
        self.progress_label.grid(row=5, column=0, columnspan=2)


        self.timer_on = False
        self.seconds_left = 0
        self.current_cycle_num = 0
        self.completed_cycles = 0
        self.total_cycles = 0


        self.mode1 = "work"
        self.time1 = 10
        self.mode2 = "short_break"
        self.time2 = 5
        self.mode3 = "work"
        self.time3 = 10
        self.mode4 = "short_break"
        self.time4 = 5
        self.mode5 = "work"
        self.time5 = 10
        self.mode6 = "long_break"
        self.time6 = 15


    def start_timer(self):
        if self.timer_on == False:
            # get cycles
            try:
                num_cycles = int(self.cycle_entry.get())
            except:
                messagebox.showerror("Invalid input", "Please type a number 1–5")
                return

            if num_cycles < 1 or num_cycles > 5:
                messagebox.showerror("Invalid number", "Enter number between 1- 5")
                return

            self.total_cycles = num_cycles
            self.progress["maximum"] = self.total_cycles
            self.progress["value"] = 0
            self.progress_label.config(text="0/" + str(self.total_cycles) + " cycles done")

            self.timer_on = True
            self.current_cycle_num = 0
            self.completed_cycles = 0

            t = threading.Thread(target=self.run_timer)
            t.start()

    def stop_timer(self):
        self.timer_on = False

    def run_timer(self):
        # create a simple list for the 6 steps
        steps = [
            ("Work", 10, "Work for 10 minutes"),
            ("Short Break", 5, "Take a 5 min break"),
            ("Work", 10, "Work for 10 minutes"),
            ("Short Break", 5, "Take a 5 min break"),
            ("Work", 10, "Work for 10 minutes"),
            ("Long Break", 15, "Take a 15 min break")
        ]

        while self.timer_on == True and self.completed_cycles < self.total_cycles:
            # get current step
            title, t_time, msg = steps[self.current_cycle_num]

            self.seconds_left = t_time
            self.frame.after(0, lambda t=title, m=msg: messagebox.showinfo(t, m))

            while self.seconds_left > 0 and self.timer_on == True:
                mins = self.seconds_left // 60
                secs = self.seconds_left % 60
                self.timer_display.config(text=str(mins).zfill(2) + ":" + str(secs).zfill(2))
                time.sleep(1)
                self.seconds_left -= 1

            # move to next step
            self.current_cycle_num += 1
            if self.current_cycle_num >= len(steps):
                self.completed_cycles += 1
                self.current_cycle_num = 0
                self.update_progress()

        if self.completed_cycles >= self.total_cycles:
            messagebox.showinfo("Completed!", "Studying done! update Progress!")
            self.timer_on = False


    def update_progress(self):
        self.progress["value"] = self.completed_cycles
        self.progress_label.config(text=str(self.completed_cycles) + "/" + str(self.total_cycles) + " cycles done")
