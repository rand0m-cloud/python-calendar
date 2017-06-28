from HelperFiles.utils import *
from googleEvent import googleEvent
from HelperFiles.utils import getInputFromList


class google:

    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
        self.calendarID = "primary"
       
    def setCalendarID(self, value):
        self.calendarID = value 

    def get_events(self, calendar_id,minTime=None,maxTime=None):
        if minTime == None:
            minTime = datetime.datetime.utcnow() # NOW!!!!
            tommorow = (minTime + datetime.timedelta(days=0)).date()
            minTime = datetime.datetime.combine(tommorow, datetime.time(hour=8))
            minTime = minTime.isoformat() + 'Z'
        #should set max Time default
        if maxTime == None:
            temp = datetime.datetime.combine(tommorow, datetime.time(hour=23))
            maxTime = temp.isoformat() + 'Z'
        #FIXME add back in maxTime
        results = self.service.events().list(calendarId=calendar_id,timeMin=minTime, orderBy="startTime", singleEvents=True).execute()
        return results["items"]

    def cleanEvents(self, events):

        cleanEvents = []  # exclude all day events

        for event in events:
            if event["start"].has_key("dateTime") == False:
                continue
            calEvent = googleEvent(event)

            cleanEvents.append(calEvent)

        return cleanEvents


    def getCalendars(self):
        return self.service.calendarList().list().execute()
      
    def select_calendar(self):
        calendarsNames = []
        calendars = []

        calendar_list = self.service.calendarList().list().execute()

        for calendar_list_entry in calendar_list['items']:
            calendarsNames.append(calendar_list_entry['summary'])
            calendars.append(calendar_list_entry)

        selectedCalendar = getInputFromList(calendars, calendarsNames)
        return selectedCalendar["id"]





