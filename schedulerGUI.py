from googleEvent import googleEvent
from unscheduledTask import *
from calendarManager import *
from Tkinter import *
from googleAPI import *
from wunderAPI import *
from schedular import *

class GUI:


    def __init__(self):

        self.google = google()
        self.wunder = wunder()

        #GUI CREATION        

        print "Creating GUI"
    
        root = Tk()

        root.title("Scheduler")
        root.geometry("300x400")

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
            if not self.wunder.listID:
                self.wunder.setListID(list["title"])
        print "Got Lists"
        WunderlistOptions.select_set(0)

        WunderlistOptions.bind('<<ListboxSelect>>', self.changeListID)
        WunderlistOptions.grid(row=1, column=0)

        #Temp do it button

        PopulateCalendar = Button(root, text="Do it", command=self.populateCalendar)

        PopulateCalendar.grid(row=2, column=0)

        root.mainloop()

    def populateCalendar(self):
        print "Filling Calendar..."
        events = self.google.get_events(self.google.calendarID)

        cleanEvents = []  # exclude all day events

        for event in events:
            if event["start"].has_key("dateTime") == False:
                continue
            calEvent = googleEvent(event)
            cleanEvents.append(calEvent)
            print calEvent

        self.schedularHandler = schedular()

        listID = self.wunder.listID

        listOfTasks = self.wunder.get_tasks(listID)

        taskToSchedule = self.wunder.parse_tasks(listOfTasks)

        if taskToSchedule != []:
            taskToSchedule = self.schedularHandler.order_tasks(taskToSchedule)

            for task in taskToSchedule:
                print task

            print "done"

            self.schedularHandler.schedule_day(cleanEvents, taskToSchedule, datetime.date.today()+datetime.timedelta(days=1), self.google.calendarID)

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
