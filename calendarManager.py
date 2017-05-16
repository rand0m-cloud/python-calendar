from utils import *
from server import *
from googleEvent import googleEvent
import httplib2
import os
import requests
from apiHandler import *
from unscheduledTask import *
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime,arrow

def get_events(calendar_id,minTime=None,maxTime=None):
    if minTime == None:
        minTime = datetime.datetime.utcnow().isoformat() + 'Z' # NOW!!!!
    #should set max Time default
    results = apiHandler.google.service.events().list(calendarId=calendar_id,timeMin=minTime,timeMax=maxTime, orderBy="startTime", singleEvents=True).execute()
    return results["items"]

def select_calendar():
    calendarsNames = []
    calendars = []

    calendar_list = apiHandler.google.service.calendarList().list().execute()

    for calendar_list_entry in calendar_list['items']:
        calendarsNames.append(calendar_list_entry['summary'])
        calendars.append(calendar_list_entry)

    selectedCalendar = getInputFromList(calendars, calendarsNames)
    return selectedCalendar["id"]

def select_list():
    listNames = []

    listOfLists = apiHandler.wunder.request("GET","http://a.wunderlist.com/api/v1/lists")

    for list in listOfLists:
        listNames.append(list["title"])

    list = getInputFromList(listOfLists,listNames)
    return list["id"]

def get_tasks(listID):
    return apiHandler.wunder.request("GET","http://a.wunderlist.com/api/v1/tasks",data={ "list_id":listID })

def change_task_name(task, title):
    apiHandler.wunder.request("PATCH", "https://a.wunderlist.com/api/v1/tasks/" + str(task["id"]),data={"revision":task["revision"], "title":title})


def parse_tasks(listOfTasks):
    tasksToSchedule = []

    for task in listOfTasks:

        print task
        title = task["title"].split('#')
        if len(title) == 1:
            continue
        change_task_name(task, title[0])
        # number - length, s-number of segements, r-repeat frequency, p-preparation time
        length = 0
        repeatsFreq = 0 #TODO Add me
        segments = 1
        prep = 0
        for bit in title:
            bit = bit.strip()
            if bit.isdigit():
                length = int(bit)
            if bit.startswith("s"):
                segments = int(bit[1:])
            if bit.startswith("r"):
                repeatsFreq = int(bit[1:])
            if bit.startswith("p"):
                prep = int(bit[1:])
        length /= segments
        while segments>0:
            tasksToSchedule.append(unscheduledTask(title[0].strip(), length, setUp=prep))
            segments-=1
    return tasksToSchedule

def order_tasks(listOfTasks):
    return listOfTasks.sort(key=lambda r: r["DueDate"])

def schedule_day(googleEvents, tasksToSchedule, date, calendarID):
    time = datetime.time(8)
    nextTask = 0

    while nextTask < len(tasksToSchedule):
        sceduled = False

        for event in googleEvents:
            timeToCheck = (datetime.datetime.combine(date, time)+ datetime.timedelta(minutes=tasksToSchedule[nextTask].length))

            if  timeToCheck < event.start.replace(tzinfo=timeToCheck.tzinfo):
                tasksToSchedule[nextTask].schedule(date, time, calendarID)
                timeToCheck+=datetime.timedelta(minutes=tasksToSchedule[nextTask].length+tasksToSchedule[nextTask].setUp)
                time = timeToCheck.time()
                nextTask+=1
                sceduled = True
                break
            else:
                time = event.end.time()

        if not sceduled:
            return -1

        if time > datetime.time(hour=23):
            return 1
    return 0



def main():
    calendarID = select_calendar()

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

    for task in taskToSchedule:
        print task

    schedule_day(cleanEvents, taskToSchedule, datetime.date.today()+datetime.timedelta(days=1), calendarID)


if __name__ == '__main__':
    main()

