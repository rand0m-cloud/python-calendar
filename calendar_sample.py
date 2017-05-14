from utils import *
from server import *
from calendarEvent import calendarEvent
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

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
global calendarID
global API
def get_events(calendar_id,minTime=None,maxTime=None):
    if minTime == None:
        minTime = datetime.datetime.utcnow().isoformat() + 'Z' # NOW!!!!
    results = get_service().events().list(calendarId=calendar_id,timeMin=minTime,timeMax=maxTime).execute()
    return results["items"]

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    #service = get_service()

    service = apiHandler.google.service
    page_token = None

    calendars = []
    calendarsNames = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendarsNames.append(calendar_list_entry['summary'])
            calendars.append(calendar_list_entry)

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    selectedCalendar = getInputFromList(calendars,calendarsNames)
    calendarID = selectedCalendar["id"]
    set_calendarID(calendarID)
    events = get_events(calendarID)


    for event in events:

        if event["start"].has_key("dateTime")==False:
                continue



        calEvent = calendarEvent(event)
        print calEvent

    #testEvent = UnscheduledTask("Potato", length=15, setUp=5)
    #testEvent.schedule(datetime.datetime.now())



    listOfLists = apiHandler.wunder.request("GET","http://a.wunderlist.com/api/v1/lists")
    i=1
    listNames = []
    for list in listOfLists:
        listNames.append(list["title"])
    list = getInputFromList(listOfLists,listNames)
    print "{}:{}".format(list["title"],list["id"])
    listOfTasks = apiHandler.wunder.request("GET","http://a.wunderlist.com/api/v1/tasks",data={
        "list_id":list["id"]
    })

    for task in listOfTasks:

        print task
        title = task["title"].split('#')
        newEvent = UnscheduledTask(title[0], int(title[1]))
        newEvent.schedule(datetime.datetime.now())

if __name__ == '__main__':
    main()

