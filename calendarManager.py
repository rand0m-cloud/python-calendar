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
        minTime = datetime.datetime.utcnow() # NOW!!!!
        tommorow = (minTime + datetime.timedelta(days=1)).date()
        minTime = datetime.datetime.combine(tommorow, datetime.time(hour=8))
        minTime = minTime.isoformat() + 'Z'
    #should set max Time default
    if maxTime == None:
        temp = datetime.datetime.utcnow()+datetime.timedelta(days=1)
        maxTime = temp.isoformat() + 'Z'
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
        fun = 0
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
            if bit.startswith("i"):
                fun = int(bit[1:])
        length /= segments
        while segments>0:
            tasksToSchedule.append(unscheduledTask(title[0].strip(), length, fun, setUp=prep))
            segments-=1
    return tasksToSchedule

def order_tasks(listOfTasks):
    orderedTasks = []
    net = 0
    length = 0
    for task in listOfTasks:
        net += task.weight
        length += task.lengthInHours
    slope = net/length
    time = 0
    weight = 0
    tasksLeft = len(listOfTasks)
    while tasksLeft > 0:
        resultDelta = []
        for task in listOfTasks:
            resultDelta.append(abs(weight+task.weight-(time+task.lengthInHours)*slope))
        choice = resultDelta.index(min(resultDelta))
        time += listOfTasks[choice].lengthInHours
        weight += listOfTasks[choice].weight
        orderedTasks.append(listOfTasks[choice])
        listOfTasks.pop(choice)
        tasksLeft-=1
    return orderedTasks

def tryToSchedule(nextTask, tasksToSchedule, date, time, event, calendarID):
    while nextTask < len(tasksToSchedule):
        timeToCheck = datetime.datetime.combine(date, time)
        timeToCheck += datetime.timedelta(minutes=tasksToSchedule[nextTask].length + tasksToSchedule[nextTask].setUp)
        if timeToCheck > event.start.replace(tzinfo=timeToCheck.tzinfo):
            return [time, nextTask]
        # there should be enough space for our event here
        tasksToSchedule[nextTask].schedule(date, time, calendarID)
        time = timeToCheck.time()
        nextTask += 1 #FIXME U SUCK
    return [23, nextTask]


#TODO add break scheduling
def scheduleBlock(timespan, startTime, tasksToSchedule, calendarID):
    while len(tasksToSchedule) > 0:
        if datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2) < timespan:
            tasksToSchedule[0].schedule(startTime.date(), (startTime+datetime.timedelta(minutes=tasksToSchedule[0].setUp)).time(), calendarID)
            timespan -= datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
            startTime += datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)
            tasksToSchedule.pop(0)
        else:
            #schedule breaks here
            return



def schedule_day(googleEvents, tasksToSchedule, date, calendarID):
    startTime = datetime.datetime.combine(date, datetime.time(hour=8))
    i = 0
    while i < len(googleEvents)-1:
        nextBlock = googleEvents[i+1].start - googleEvents[i].end
        if(nextBlock > datetime.timedelta(minutes=tasksToSchedule[0].length+tasksToSchedule[0].setUp*2)):
            scheduleBlock(nextBlock, googleEvents[i].end, tasksToSchedule, calendarID)
        i += 1


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

    taskToSchedule = order_tasks(taskToSchedule)

    for task in taskToSchedule:
        print task

    schedule_day(cleanEvents, taskToSchedule, datetime.date.today()+datetime.timedelta(days=1), calendarID)


if __name__ == '__main__':
    main()

