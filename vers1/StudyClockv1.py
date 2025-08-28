import time
from tkinter import *
import threading
import json
from tkinter import ttk

class StudyClock:
    def __init__(self,parent):
        # create a frame inside the parent window
        self.frame=Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")  
        self.root = parent   # keep a reference to the parent

        # label that shows the timer (default = 10:00)
        self.timer_label = Label(self.root, text="10:00", font="Arial 17")
        self.timer_label.grid(pady=10, padx=10)

        # load tasks from json file and prepare dropdown list
        self.tasks = self.load_tasks()
        self.tasks_var = StringVar()
        task_names = [task["Project Name"] for task in self.tasks] or ["no available tasks."]

        # frame to hold the start/pause buttons
        btn_frame = Frame(self.frame)
        btn_frame.grid(pady=10)

        # label and dropdown menu for choosing a task
        task_label = Label(self.frame, text="Select Tasks", font="Arial 17")
        task_label.grid(row=0, column=1)

        self.tasks_menu = ttk.Combobox(self.frame, textvariable=self.tasks_var, values=task_names, state="readonly")
        self.tasks_menu.current(0)  # select first task by default
        self.tasks_menu.grid(row=0, column=1)

        # start + pause buttons
        self.startbtn = Button(btn_frame, text="Start", width=10, command=self.start_timer)
        self.startbtn.grid(row=0, column=0, padx=10)

        self.pausebtn = Button(btn_frame, text="Pause", width=10, command=self.pause_timer, state=DISABLED)
        self.pausebtn.grid(row=0, column=1, padx=10)

        # timer variables
        self.is_running = False
        self.default_time = 10 * 60  # 10 minutes in seconds
        self.remaining_time = self.default_time

    # read the tasks.json file and return the tasks list
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as task_file:
                return json.load(task_file)
        except:
            return []   # return empty if file not found / invalid

    # start the countdown
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.startbtn.config(state=DISABLED)
            self.pausebtn.config(state=NORMAL)

            t = threading.Thread(target=self.countdown, daemon=True)
            t.start()

    # pause/stop the countdown
    def pause_timer(self):
        self.is_running = False
        self.startbtn.config(state=NORMAL)
        self.pausebtn.config(state=DISABLED)

    # format seconds into mm:ss string
    def format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    # actual countdown logic
    def countdown(self):
        while self.remaining_time >= 0 and self.is_running:
            self.timer_label.config(text=self.format_time(self.remaining_time))
            time.sleep(1)                 # wait 1 sec
            self.remaining_time -= 1      # subtract 1 sec from total time

        # when timer hits 0
        if self.remaining_time < 0:
            self.timer_label.config(text="Time is up!")
            self.is_running = False
            self.startbtn.config(state=NORMAL)
            self.pausebtn.config(state=DISABLED)
            self.remaining_time = self.default_time  # reset for next study session
