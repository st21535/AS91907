import json
from tkinter import *
from tkinter import ttk, messagebox


class StudyClock:
    def __init__(self, parent):
        # Main container stores inside the parent window
        self.frame = Frame(parent, bg="#f0f2f5")
        self.frame.pack(fill="both", expand=True)

        # A secondary frame centered inside parent window. All GUI goes here
        # (to center align)
        self.center_frame = Frame(self.frame, bg="#ffffff", padx=25, pady=25)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Loading tasks from the JSON
        self.tasks = []
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except Exception:
            self.tasks = []

        # Taking the project names from the list
        task_names = [t["Project Name"] for t in self.tasks]
        if not task_names:
            task_names = ["No tasks-Enter Task"]  # If no tasks exist, display message
            messagebox.showerror("No Task", "You have no pending tasks. Clock will stil work but we reccomend you have a goal to work towards")

        # Drop down for selecting task
        self.selected_task = StringVar()
        self.selected_task.set(task_names[0])  # This is the default option
        Label(
            self.center_frame,
            text="Select Task:",
            font=("verdana", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))
        self.task_dropdown = ttk.Combobox(
            self.center_frame,
            textvariable=self.selected_task,
            values=task_names,
            state="readonly",
            font=("verdana", 12),
            justify="center",
        )
        self.task_dropdown.pack(fill="x", pady=(0, 10))

        # The Entry box for how many pomo-cycles the user wants
        Label(
            self.center_frame,
            text="How many cycles (max 5):",
            font=("verdana", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 5))
        self.cycle_entry = Entry(
            self.center_frame,
            font=("verdana", 12),
            justify="center",
            bd=1,
            highlightthickness=1,
            highlightbackground="#d0d0d0",
        )
        self.cycle_entry.insert(0, "1")  # Default cycle 1
        self.cycle_entry.pack(pady=(0, 10))

        # Timer Display label starting at 00:00
        self.timer_display = Label(
            self.center_frame,
            text="00:00",
            font=("verdana", 36, "bold"),
            bg="#ffffff",
            fg="#46FF96",
        )
        self.timer_display.pack(pady=(0, 15))

        # The start and pause buttons in a separate small frame
        button_frame = Frame(self.center_frame, bg="#ffffff")
        button_frame.pack(pady=(0, 15))
        self.start_btn = Button(
            button_frame,
            text="Start",
            font=("verdana", 13),
            bg="#4CAF50",
            fg="#ffffff",
            bd=0,
            width=10,
            command=self.start_timer,
        )
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = Button(
            button_frame,
            text="Stop",
            font=("verdana", 13),
            bg="#f44336",
            fg="#ffffff",
            bd=0,
            width=10,
            command=self.stop_timer,
        )
        self.stop_btn.pack(side="left", padx=5)

        # Progress bar
        self.progress_var = DoubleVar()
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor="#e0e0e0",
            background="#4CAF50",
            thickness=20,
        )
        self.progress_bar = ttk.Progressbar(
            self.center_frame,
            length=300,
            variable=self.progress_var,
            style="green.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=(10, 0))
        self.progress_label = Label(
            self.center_frame, text="0/0 cycles done", font=("verdana", 12), bg="#ffffff"
        )
        self.progress_label.pack(pady=(0, 5))

        # The variables for timer state
        self.timer_on = False
        self.seconds_left = 0
        self.current_cycle_num = 0
        self.completed_cycles = 0
        self.total_cycles = 0

        # Preset modes. These are set values
        self.mode1, self.time1 = "work", 10
        self.mode2, self.time2 = "short_break", 5
        self.mode3, self.time3 = "work", 10
        self.mode4, self.time4 = "short_break", 5
        self.mode5, self.time5 = "work", 10
        self.mode6, self.time6 = "long_break", 15

        # Steps preset
        self.steps = [
            ("Work", 10, "Work for 10 minutes"),
            ("Short Break", 5, "Take a 5 min break"),
            ("Work", 10, "Work for 10 minutes"),
            ("Short Break", 5, "Take a 5 min break"),
            ("Work", 10, "Work for 10 minutes"),
            ("Long Break", 15, "Take a 15 min break"),
        ]

    def start_timer(self):
        # If the timer is not already on, turn on
        if not self.timer_on:
            try:
                num_cycles = int(self.cycle_entry.get())
            except Exception:
                messagebox.showerror("Invalid input", "Please type a number 1–5")
                return

            # If the number cycles are not between 1-5, raise error
            if num_cycles < 1 or num_cycles > 5:
                messagebox.showerror("Invalid number", "Enter number between 1-5")
                return

            # Reset cycle progress
            self.total_cycles = num_cycles
            self.progress_bar["maximum"] = self.total_cycles
            self.progress_var.set(0)
            self.progress_label.config(
                text=f"0/{self.total_cycles} cycles done"
            )

            # Reset timer state
            self.timer_on = True
            self.current_cycle_num = 0
            self.completed_cycles = 0
            self.next_step()  # start first step

    def stop_timer(self):
        # Stops timer
        self.timer_on = False

    def next_step(self):
        # Start next step if timer is on
        if not self.timer_on:
            return

        if self.completed_cycles >= self.total_cycles:
            messagebox.showinfo("Completed!", "Studying done! Update Progress!")
            self.timer_on = False
            return

        # Getting the current step
        title, duration, msg = self.steps[self.current_cycle_num]
        if "Break" in title:
            self.timer_display.config(fg="#4DA3FA") 
        else:
            self.timer_display.config(fg="#46FF96")    
        self.seconds_left = duration# *60 to do mins, testing with seconds

        # Pop up information after each step - for visual aid
        self.frame.after(0, lambda t=title, m=msg: messagebox.showinfo(t, m))

        # Countdown loop using after()
        self.countdown_step()

    def countdown_step(self):
        # Non-blocking countdown
        if not self.timer_on:
            return

        if self.seconds_left > 0:
            mins = self.seconds_left // 60
            secs = self.seconds_left % 60
            self.timer_display.config(
                text=f"{str(mins).zfill(2)}:{str(secs).zfill(2)}"
            )
            self.seconds_left -= 1
            #If testing, change 1000 to 200m otherwise keep at 1000
            self.frame.after(200, self.countdown_step) 
        else:
            # Moving on to the next step
            self.current_cycle_num += 1
            if self.current_cycle_num >= len(self.steps):
                self.completed_cycles += 1
                self.current_cycle_num = 0
                self.update_progress()
            self.next_step()

    def update_progress(self):
        # Updates the progress bar
        self.progress_var.set(self.completed_cycles)
        self.progress_label.config(
            text=f"{self.completed_cycles}/{self.total_cycles} cycles done"
        )