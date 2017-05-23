from googleEvent import googleEvent
from unscheduledTask import *
from calendarManager import *
from Tkinter import *
from googleAPI import *
from wunderAPI import *

class GUI:


    def __init__(self):

        self.google = google()
        self.wunder = wunder()


        root = Tk()

        GoogleFrame = Frame(root)
        WunderFrame = Frame(root)
        ActionFrame = Frame(root)

        GoogleCalendarOptions = Listbox(GoogleFrame, selectmode=SINGLE)
        for event in self.google.getCalendars()["items"]:
            GoogleCalendarOptions.insert(END, event["summary"])

        GoogleCalendarOptions.select_set(0)

        GoogleCalendarOptions.bind('<<ListboxSelect>>', self.changeCalendarID)
        GoogleCalendarOptions.pack(side=TOP)

        GoogleFrame.pack(side=LEFT)
        WunderFrame.pack(side=LEFT)
        ActionFrame.pack(side=LEFT)

        root.mainloop()

    def changeCalendarID(self, event):
        lb = event.widget
        index = int(lb.curselection()[0])
        value = lb.get(index)
        print value
        self.google.setCalendarID(value)

