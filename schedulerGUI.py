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

        #GUI CREATION        

        print "Creating GUI"
    
        root = Tk()
        
        #Calendar Selection Box

        GoogleCalendarOptions = Listbox(root, selectmode=SINGLE, exportselection=0)
        
        for event in self.google.getCalendars()["items"]:
            GoogleCalendarOptions.insert(END, event["summary"])

        GoogleCalendarOptions.select_set(0)

        GoogleCalendarOptions.bind('<<ListboxSelect>>', self.changeCalendarID)
        GoogleCalendarOptions.grid(row=0, column=0)

        #Wunderlist Selection Box

        print "Creating Wunderlist Box"

        WunderlistOptions = Listbox(root, selectmode=SINGLE, exportselection=0)

        for list in self.wunder.getLists():
            WunderlistOptions.insert(END, list["title"])
        
        print "Got Lists"

        WunderlistOptions.select_set(0)

        WunderlistOptions.bind('<<ListboxSelect>>', self.changeListID)
        WunderlistOptions.grid(row=1, column=0)

        root.mainloop()

    def changeListID(self, event):
        lb = event.widget
        index = int(lb.curselection()[0])
        value = lb.get(index)
        print value
        self.wunder.setListID(value)

    def changeCalendarID(self, event):
        lb = event.widget
        index = int(lb.curselection()[0])
        value = lb.get(index)
        print value
        self.google.setCalendarID(value)

