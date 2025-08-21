'''
Working
-clock
buttons
need to add
-fix start(when start dont reset)
pomodorro technique
lock in mode



'''

import time
from tkinter import *
import threading
import json
from tkinter import ttk
class StudyClock:
    def __init__(self):
        self.root=Tk()
        self.root.geometry("600x400")
        self.root.title("Study Clock")

        self.timer_label=Label(self.root,text="10:00",font="Arial 17")
        self.timer_label.grid(pady=10,padx=10)

        self.tasks=self.load_tasks()
        self.tasks_var=StringVar()
        task_names=[]
        for task in self.tasks:
            task_names.append(task["Project Name"])
        if not task_names:
            task_names=["no availiable tasks."]

        btn_frame=Frame(self.root)
        btn_frame.grid(pady=10)

        self.is_running = False
        self.default_time=10*60
        self.seconds_left=self.default_time



        task_label=Label(self.root,text="Select Tasks",font="arial 17")
        task_label.grid(row=0,column=1)

        self.tasks_menu=ttk.Combobox(self.root,textvariable=self.tasks_var,values=task_names,state="Readonly")
        self.tasks_menu.current(0)
        self.tasks_menu.grid(row=0,column=1)

        self.startbtn=Button(btn_frame,text="Start",width=10,command=self.start_timer)
        self.startbtn.grid(row=0,column=0,padx=10)

        self.pausebtn=Button(btn_frame,text="Pause",width=10,command=self.pause_timer,state=DISABLED)
        self.pausebtn.grid(row=0,column=1,padx=10)


    def load_tasks(self):
        try:
           with open("tasks.json","r") as task_file:
               return json.load(task_file)
        except:
            return[]
        
    def start_timer(self):
        if not self.is_running:
            self.is_running=True
            self.startbtn.config(state=DISABLED)
            self.pausebtn.config(state=NORMAL)
            
            t = threading.Thread(target=self.countdown, daemon=True)
            t.start()
    def pause_timer(self):
            self.is_running=False
            self.startbtn.config(state=NORMAL)
            self.pausebtn.config(state=DISABLED)
    '''def lockin(self):
            if not self.is_running:
                self.is_running=True
                self.startbtn.config(state=DISABLED)
                self.pausebtn.config(state=DISABLED)'''

    def format_time(self,total_seconds):

        minutes=total_seconds //60
        seconds=total_seconds%60
        return f"{minutes:02}:{seconds:02}"


    def countdown(self):

        while self.seconds_left >=0 and self.is_running:
            self.timer_label.config(text=self.format_time(self.seconds_left))
            time.sleep(1)
            self.seconds_left-=1

        if self.seconds_left<0:
            self.timer_label.config(text="Time is up!")
            self.is_running=False
            self.startbtn.config(state=NORMAL)
            self.pausebtn.config(state=DISABLED)
            self.seconds_left=self.default_time
    def run(self):
        self.root.mainloop()

StudyClock().run()