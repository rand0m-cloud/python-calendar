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
    results = apiHandler.google.service.events().list(calendarId=calendar_id,timeMin=minTime,timeMax=maxTime).execute()
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

def parse_tasks(listOfTasks):
    tasksToSchedule = []

    for task in listOfTasks:

        print task
        title = task["title"].split('#')
        if len(title) == 1:
            continue
        tasksToSchedule.append(unscheduledTask(title[0].strip(), int(title[1])))

    return tasksToSchedule

def translate_events(googleEvents):
    newEvents = []

    for event in googleEvents:
        newEvents.append(googleEvent(event))

    return newEvents

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


if __name__ == '__main__':
    main()

