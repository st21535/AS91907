from tkinter import *

class StudyClock:
    def __init__(self):
        self.root = Tk()
        self.root.title("Study Buddy")

        self.container = Frame(self.root)
        self.container.grid(row=0,column=0,sticky="nswe")


        self.frames = {}

        self.frames["MainFrame"] = self.create_main_frame()
        self.frames["AddTask"] = self.create_to_addtask()
        self.frames["Tracker"] = self.create_to_tracker()
        self.frames["StudyClock"] = self.create_to_clock()
        
        self.show_frame("MainFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        
    def create_main_frame(self):
        frame = Frame(self.container)

        self.main_title_label=Label(frame,font="Arial 16", text="Study Buddy!")
        self.main_title_label.grid(row=0,columnspan=3,padx=10,pady=10)

        self.to_task_button=Button(frame, text="To Tracker",font="Arial 12",command=lambda:self.show_frame("Tracker"))
        self.to_task_button.grid(row=1,column=0,padx=10,pady=10)

        self.to_task_button=Button(frame, text="To task adder",font="Arial 12",command=lambda:self.show_frame("AddTask"))
        self.to_task_button.grid(row=1,column=1,padx=10,pady=10)

        self.to_task_button=Button(frame, text="StudyClock",font="Arial 12",command=lambda:self.show_frame("StudyClock"))
        self.to_task_button.grid(row=1,column=2,padx=10,pady=10)
        frame.grid(row=0, column=0, sticky="nswe")
        return frame

    def create_to_addtask(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")

        
        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame
    def create_to_tracker(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)
        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame
    def create_to_clock(self):
        frame = Frame(self.container)
        self.title=Label(frame,font="Arial 16", text="Haro")
        self.title.grid(row=0,columnspan=3,padx=10,pady=10)

        self.back_button=Button(frame, text="BAck",font="Arial 12",command=lambda:self.show_frame("MainFrame"))
        self.back_button.grid(row=1,column=0,padx=10,pady=10)

        frame.grid(row=0, column=0, sticky="nswe")

        return frame




    def run(self):
        self.root.mainloop()

StudyClock().run()