from googleEvent import googleEvent
from unscheduledTask import *
from calendarManager import *
from Tkinter import *

class GUI:
    def __init__(self):
        self.calendarID = "primary"

        root = Tk()

        GoogleFrame = Frame(root)
        WunderFrame = Frame(root)
        ActionFrame = Frame(root)

        GoogleCalendarOptions = Listbox(GoogleFrame, selectmode=SINGLE)
        for event in getCalendars()["items"]:
            GoogleCalendarOptions.insert(END, event["summary"])
        GoogleCalendarOptions.select_set(0)
        GoogleCalendarOptions.bind('<<ListboxSelect>>', changeCalendarID)
        GoogleCalendarOptions.pack(side=TOP)

        GoogleFrame.pack(side=LEFT)
        WunderFrame.pack(side=LEFT)
        ActionFrame.pack(side=LEFT)

        root.mainloop()
