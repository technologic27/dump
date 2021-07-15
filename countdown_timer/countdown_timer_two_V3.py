from tkinter import *
import datetime
import time

#5 minutes later red color

class Application(Frame):
    def __init__(self, master):

        super(Application, self).__init__(master)
        self.grid()
        self.createWidgets()
        self._alarm_id = None
        self._paused = False
        self._starttime = 0
        self._elapsedtime = 0
        self.resize_factor = 5


    def createWidgets(self):
    
        #change word reset factor here
        resize_factor = 12
        self.topFrame = Frame(self)
        #self.someFrame.pack(side=TOP)
        self.topFrame.grid(columnspan = 1)
       
        #self.bottomFrame = Frame(self)
        #self.bottomFrame.grid(columnspan = 7)

        self.Title = Label(self.topFrame, text="EX CYBERARK", font=("arial", 40+resize_factor, "bold"), fg="black", bg=None)
        self.Title.grid(row=0, column=1, columnspan = 7)
        #self.Title.pack(fill=X)
        self.Title = Label(self.topFrame, text="MARITIME SECTOR", font=("arial", 40+resize_factor, "bold"), fg="black", bg=None)
        self.Title.grid(row=1, column=1, columnspan = 7)

        #self.spacer6 = Label(self.topFrame, text = " ")
        #self.spacer6.grid(row = 2)

        self.moveLabel = Label(self.topFrame, text = "MOVE", font=("arial", 20+resize_factor), fg="black", bg=None)
        self.moveEntry = Entry(self.topFrame, font=("arial", 20+resize_factor), width=1, fg="black", bg=None)
        self.moveLabel.grid(row=3, column=1, columnspan = 1)
        self.moveEntry.grid(row=4, column=1, columnspan = 1)
        #self.moveLabel.pack(side=LEFT, expand=NO, pady=2, padx =2)
        #self.moveEntry.pack(side=LEFT, expand=NO, pady =2, padx = 2)
        self.moveEntry.bind('<Return>', self.moveEntry.get())

        self.injectLabel = Label(self.topFrame, text = "EVENT", font=("arial", 20+resize_factor), fg="black", bg=None)
        self.injectEntry = Entry(self.topFrame, font=("arial", 20+resize_factor), width=1, fg="black", bg="white")
        self.injectLabel.grid(row=3, column=2, columnspan = 1)
        self.injectEntry.grid(row=4, column=2, columnspan = 1)
        self.injectEntry.bind('<Return>', self.injectEntry.get())

        self.commLabel = Label(self.topFrame, text = "CRISIS COMM", font=("arial", 20+resize_factor), fg="black", bg=None)
        self.commEntry = Entry(self.topFrame, font=("arial", 20+resize_factor), width=1, fg="black", bg="white")
        self.commLabel.grid(row=3, column=4, columnspan = 2)
        self.commEntry.grid(row=4, column=4, columnspan = 2)

        self.commEntry.bind('<Return>', self.commEntry.get())

        self.spacer8 = Label(self.topFrame, text = " ")
        self.spacer8.grid(row = 5)

        self.spacer8 = Label(self.topFrame, text = " ")
        self.spacer8.grid(row = 6)
        
        #self.typeEntry = Entry(self.topFrame, font=("arial", 20+resize_factor), width=5+resize_factor, fg="black", bg="white")
        #self.typeEntry.grid(row=6, column=3, sticky = "nsew")
        #self.typeEntry.bind('<Return>', self.typeEntry.get())

        self.dropDownVar0 = StringVar()
        self.dropDownVar0.set("DISCUSSION") # default value
        self.dropDown0 = OptionMenu(self.topFrame, self.dropDownVar0, "DISCUSSION", "RESPONSE", "LUNCH", "BREAK")
        self.dropDown0.config(font=("arial", 15+resize_factor),width=5+resize_factor)
        self.dropDown0.grid(row=8, column=1,sticky = 'w')


        
        self.dropDownVar = StringVar()
        self.dropDownVar.set("NCTAL (YELLOW)") # default value
        self.dropDown = OptionMenu(self.topFrame, self.dropDownVar, "NCTAL (YELLOW)", "NCTAL (ORANGE)", "NCTAL (RED)")
        self.dropDown.config(font=("arial", 15+resize_factor),width=5+resize_factor, fg = "black")
        self.dropDown.grid(row=6, column=1, sticky = 'w')
        Callbackname = self.dropDownVar.trace_variable("w", self.callbackFunc)
        #self.dropDown.pack()

        self.space6 = Label(self.topFrame, text = " ")
        self.space6.grid(row = 7)

        self.countDownLabel = Label(self.topFrame, text = "COUNTDOWN", font=("arial", 20+resize_factor), fg="black", bg= None)
        self.countDownLabel.grid(row=6, column=3, columnspan=5)

        self.labelvariable = StringVar()
        self.labelvariable.set("00:00")
        self.thelabel = Label(self.topFrame, textvariable = self.labelvariable, font=('arial',100+resize_factor), height=2, width = 4, fg="green", bg = "black")
        self.thelabel.grid(row=8, column=3, sticky = 'nsew', rowspan=5, columnspan=5)

        #self.spacer2 = Label(self.topFrame, text = " ")
        #self.spacer2.grid(row = 10)

        #self.elapsedLabel = Label(self.topFrame, text = "ELAPSED", font=("arial", 10+resize_factor), fg="black", bg="white")
        #self.elapsedLabel.grid(row=11, column=3)

        #self.labelvariable2 = StringVar()
        #self.labelvariable2.set("00:00")
        #self.thelabel2 = Label(self.topFrame, textvariable = self.labelvariable2,font=('arial',50+resize_factor), height=2, fg="green", bg = "black")
        #self.thelabel2.grid(row=12, column=3, sticky = 'nsew')

        #self.thelabel2.pack(side=TOP, pady=2, padx=2)


        #self.spacer13 = Label(self.topFrame, text = " ")
        #self.spacer13.grid(row = 13)


        #self.spacer14 = Label(self.topFrame, text = " ")
        #self.spacer14.grid(row = 14)


        #self.spacer15 = Label(self.topFrame, text = " ")
        #self.spacer15.grid(row = 15)

        #self.spacer16 = Label(self.topFrame, text = " ")
        #self.spacer16.grid(row = 16)
        
        self.spacer17 = Label(self.topFrame, text = " ")
        self.spacer17.grid(row = 17)
        
        self.startButton = Button(self.topFrame, text="START",command=self.startTime, font=('arial',8+resize_factor), width=5, height=1, fg = "black")
        self.startButton.grid(row=18, column=3)
        #self.startButton.pack(side=LEFT, pady=2, padx=2)

        self.stopButton = Button(self.topFrame, text="STOP", command=self.stopTime, font=('arial',8+resize_factor), width=5, height=1, fg = "black")
        self.stopButton.grid(row=18, column=5, sticky= 'w')
        #self.stopButton.pack(side=LEFT, pady=2, padx=2)

        self.resetButton = Button(self.topFrame, text="RESET", command=self.resetTime, font=('arial',8+resize_factor), width=5, height=1, fg = "black")
        self.resetButton.grid(row=18, column=7)
        #self.resetButton.pack(side=LEFT, pady=2, padx=2)

        self.strTime = StringVar(self.topFrame, value=' 5')
        self.timeEntry = Entry(self.topFrame, textvariable= self.strTime, font=("arial", 15+resize_factor), width=2, fg="black", bg="white")
        self.timeEntry.grid(row=18, column=2)
        self.timeEntry.bind('<Return>', self.timeEntry.get())
        #time = self.timeEntry.get()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def callbackFunc(self, name, index, mode):
        value = self.dropDownVar.get()
        if value == 'NCTAL (YELLOW)':
            self.dropDown.config(bg='yellow',fg='black')
        if value == "NCTAL (ORANGE)":
            self.dropDown.config(bg='orange',fg='black')
        if value == "NCTAL (RED)":
            self.dropDown.config(bg='red',fg='black')

    def startTime(self):
        """ Resume """
        self._paused = False
        if self._alarm_id is None:
            self.countdown(int(app.timeEntry.get())*60)
            #self.countup(self._elapsedtime)

    def stopTime(self):
        """ Pause """
        if self._alarm_id is not None:
            self._paused = True

    def resetTime(self):
        """ Restore to last countdown value. """
        if self._alarm_id is not None:
            self._paused = False
            self.master.after_cancel(self._alarm_id)
            self._alarm_id = None
        mins, secs = divmod(int(app.timeEntry.get())*60, 60)
        timeformat = "{0:02d}:{1:02d}".format(mins, secs)
        app.labelvariable.set(timeformat)
        self._paused = True


    def countdown(self, timeInSeconds, start=True):

        if start:
            self._starttime = timeInSeconds
        if self._paused:
            app.thelabel.config(bg="black", fg = "green")
            self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds, False)
        else:
            app.thelabel.config(bg="black", fg = "green")
            mins, secs = divmod(timeInSeconds, 60)
            if mins == 0 and secs == 0:
                app.labelvariable.set("STOP")
                self._paused = True
            else:
                timeformat = "{0:02d}:{1:02d}".format(mins, secs)
                app.labelvariable.set(timeformat)
                self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds-1)
                if mins <= 5:
                    app.thelabel.config(bg="red", fg = "black")
            
                    #self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds-1)
                #if mins == 0 and secs == 0:
                    #app.labelvariable.set("STOP")
                #self._paused = True



    """
        
    def countup(self, timeInSeconds, start=True):
        if start:
            self._elapsedtime = timeInSeconds
        if self._paused:
            self._alarm_id = self.master.after(1000, self.countup, timeInSeconds, False)
        else:
            mins, secs = divmod(timeInSeconds, 60)
            timeformat = "{0:02d}:{1:02d}".format(mins, secs)
            app.labelvariable2.set(timeformat)
            self._alarm_id = self.master.after(1000, self.countup, timeInSeconds+1, False)
    """


            
if __name__ == '__main__':
    global root
    root = Tk()
    root.title("Trident")
    app = Application(root)

    resize_factor=app.resize_factor
    
    #change the width, height size here 
    width = 100*resize_factor
    height = 100*resize_factor
  
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    
    root.mainloop()
