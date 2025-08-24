import time
from tkinter import *
import threading
import json
from tkinter import ttk
from tkinter import messagebox

class StudyClock:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")  
        self.root = parent

        # Timer label
        self.timer_label = Label(self.frame, text="10:00", font="Arial 17")
        self.timer_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Load tasks for dropdown
        self.tasks = self.load_tasks()
        self.tasks_var = StringVar()
        task_names = [task["Project Name"] for task in self.tasks]
        if not task_names:
            task_names = ["no available tasks"]

        task_label = Label(self.frame, text="Select Task", font="Arial 17")
        task_label.grid(row=1, column=0)
        self.tasks_menu = ttk.Combobox(self.frame, textvariable=self.tasks_var, values=task_names, state="readonly")
        self.tasks_menu.current(0)
        self.tasks_menu.grid(row=1, column=1)

        # Buttons
        btn_frame = Frame(self.frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.startbtn = Button(btn_frame, text="Start", width=10, command=self.start_timer)
        self.startbtn.grid(row=0, column=0, padx=10)
        self.pausebtn = Button(btn_frame, text="Pause", width=10, command=self.pause_timer, state=DISABLED)
        self.pausebtn.grid(row=0, column=1, padx=10)

        # Pomodoro variables
        self.is_running = False
        self.current_mode = "work"  # work / short_break / long_break
        self.pomodoro_tracker = 0   # counts work sessions completed

        self.work_time = 10 
        self.short_break = 5 
        self.long_break = 15 
        self.seconds_left = self.work_time  # 10min default work session


        self.thread = None

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as task_file:
                return json.load(task_file)
        except:
            return []

    # ✅ Start timer with validation
    def start_timer(self):
        if self.is_running:
            messagebox.showwarning("Timer Running", "Timer is already running!")
            return
        self.is_running = True
        self.startbtn.config(state=DISABLED)
        self.pausebtn.config(state=NORMAL)
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.countdown_loop, daemon=True)
            self.thread.start()

    def pause_timer(self):
        self.is_running = False
        self.startbtn.config(state=NORMAL)
        self.pausebtn.config(state=DISABLED)

    def format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    # ✅ Pomodoro cycle logic
    def countdown_loop(self):
        while self.is_running:
            if self.seconds_left > 0:
                self.timer_label.config(text=self.format_time(self.seconds_left))
                time.sleep(1)
                self.seconds_left -= 1
            else:
                # End of session
                if self.current_mode == "work":
                    self.pomodoro_tracker += 1
                    if self.pomodoro_tracker % 3 == 0:
                        self.current_mode = "long_break"
                        self.seconds_left = self.long_break
                        messagebox.showinfo("Break Time!", "Long break! 15 minutes")
                    else:
                        self.current_mode = "short_break"
                        self.seconds_left = self.short_break
                        messagebox.showinfo("Break Time!", "Short break! 5 minutes")
                else:
                    # Finished a break, go back to work
                    self.current_mode = "work"
                    self.seconds_left = self.work_time
                    messagebox.showinfo("Work Time!", "Back to work! 10 minutes")

            # Update UI
            self.timer_label.config(text=self.format_time(self.seconds_left))

        # Reset buttons if paused
        self.startbtn.config(state=NORMAL)
        self.pausebtn.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    StudyClock(root)
    root.mainloop()