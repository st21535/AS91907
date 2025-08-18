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
            task_names=["There are no availiable tasks. Go to Task manager to Add"]
        btn_frame=Frame(self.root)
        btn_frame.grid(pady=10)
        self.is_running = False



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
            task=open("tasks.json", "r")
            content=task.read()
            task.close()
            tasks=json.loads(content)
            return tasks
        except:
            return[]
    def start_timer(self):
        if not self.is_running:
            self.is_running=True
            self.startbtn.config(state=DISABLED)
            self.pausebtn.config(state=NORMAL)
            
            t = threading.Thread(target=self.countdown, args=(10*60,), daemon=True)
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

        minutes=0
        seconds=0
        minutes=total_seconds //60
        seconds=total_seconds - (minutes * 60)

        if minutes <10:
            minute= "0" + str(minutes)
        else:
            minute=str(minutes)
        if seconds <10:
            second= "0" +str(seconds)
        else:
            second=str(seconds)
        return minute + ":" + second

    def countdown(self,total_seconds):
        seconds_left=total_seconds
        while seconds_left >=0 and self.is_running:
            time_text=self.format_time(seconds_left)
            self.timer_label.config(text=time_text)

            time.sleep(1)
            seconds_left=seconds_left-1

        if seconds_left<0:
            self.timer_label.config(text="Time is up!")
            self.is_running=False
            self.startbtn.config(state=NORMAL)
            self.pausebtn.config(state=DISABLED)
    def run(self):
        self.root.mainloop()

StudyClock().run()