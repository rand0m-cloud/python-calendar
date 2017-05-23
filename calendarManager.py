from googleEvent import googleEvent
from unscheduledTask import *
from schedulerGUI import *
from Tkinter import *


def oldmain():

    events = get_events(calendarID)

    cleanEvents = [] #exclude all day events

    for event in events:
        if event["start"].has_key("dateTime")==False:
                continue
        calEvent = googleEvent(event)
        cleanEvents.append(calEvent)
        print calEvent


    listID = select_list()

    listOfTasks = get_tasks(listID)

    taskToSchedule = parse_tasks(listOfTasks)

    taskToSchedule = order_tasks(taskToSchedule)

    for task in taskToSchedule:
        print task

    schedule_day(cleanEvents, taskToSchedule, datetime.date.today()+datetime.timedelta(days=1), calendarID)

def main():
    gui = GUI()

if __name__ == '__main__':
    main()

