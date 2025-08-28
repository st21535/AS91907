
'''
V2 Validation
'''
import time
import threading
from tkinter import *
from tkinter import ttk, messagebox
import json

class StudyClock:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # TASK DROPDOWN AT TOP

        self.tasks = []
        try:
            with open("tasksv2.json", "r") as f:
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

        # ENTRY BOX FOR CYCLES
        self.cycles_label = Label(self.frame, text="How many cycles (max 5):", font=("Arial", 12))
        self.cycles_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.cycle_entry = Entry(self.frame)
        self.cycle_entry.insert(0, "1")
        self.cycle_entry.grid(row=1, column=1, padx=10, pady=5)

        # TIMER DISPLAY
        self.timer_display = Label(self.frame, text="00:00", font=("Arial", 20))
        self.timer_display.grid(row=2, column=0, columnspan=2, pady=10)

        # START / STOP BUTTONS
        self.start_btn = Button(self.frame, text="Start", width=10, command=self.start_timer)
        self.start_btn.grid(row=3, column=0, pady=5)
        self.stop_btn = Button(self.frame, text="Stop", width=10, command=self.stop_timer)
        self.stop_btn.grid(row=3, column=1, pady=5)

        # PROGRESS BAR
        self.progress = ttk.Progressbar(self.frame, length=200)
        self.progress.grid(row=4, column=0, columnspan=2, pady=10)
        self.progress_label = Label(self.frame, text="0/0 cycles done")
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # STATES
        self.is_running = False
        self.seconds_left = 0
        self.step_in_cycle = 0
        self.done_cycles = 0
        self.total_cycles = 0

        # FIXED PLAN (LOCKED TIMES)
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

    # TIMER LOGIC
    def start_timer(self):
        if self.is_running == False:
            # get cycles
            try:
                num = int(self.cycle_entry.get())
            except:
                messagebox.showerror("Invalid input", "Please type a number 1–5")
                return

            if num < 1 or num > 5:
                messagebox.showerror("Invalid number", "Enter number between 1 and 5")
                return

            self.total_cycles = num
            self.progress["maximum"] = self.total_cycles
            self.progress["value"] = 0
            self.progress_label.config(text="0/" + str(self.total_cycles) + " cycles done")

            self.is_running = True
            self.step_in_cycle = 0
            self.done_cycles = 0

            t = threading.Thread(target=self.run_timer)
            t.start()

    def stop_timer(self):
        self.is_running = False

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

        while self.is_running == True and self.done_cycles < self.total_cycles:
            # get current step
            title, duration, msg = steps[self.step_in_cycle]

            self.seconds_left = duration * 60
            self.frame.after(0, lambda t=title, m=msg: messagebox.showinfo(t, m))

            while self.seconds_left > 0 and self.is_running == True:
                mins = self.seconds_left // 60
                secs = self.seconds_left % 60
                self.timer_display.config(text=str(mins).zfill(2) + ":" + str(secs).zfill(2))
                time.sleep(1)
                self.seconds_left -= 1

            # move to next step
            self.step_in_cycle += 1
            if self.step_in_cycle >= len(steps):
                self.done_cycles += 1
                self.step_in_cycle = 0
                self.update_progress()

        if self.done_cycles >= self.total_cycles:
            messagebox.showinfo("Done!", "All cycles complete 🎉")
            self.is_running = False


    def update_progress(self):
        self.progress["value"] = self.done_cycles
        self.progress_label.config(text=str(self.done_cycles) + "/" + str(self.total_cycles) + " cycles done")