import datetime
from utils import *
from apiHandler import *
import dateutil.parser

class unscheduledTask:



    def __init__(self,title, length, setUp=0):
        self.title = title
        self.length = length
        self.setUp = setUp

    def schedule(self, startTime, calendarID):
        startTimeString = startTime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
        endTime = startTime+datetime.timedelta(minutes=self.length)

        endTimeString = endTime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
        event = {
            'summary': self.title,

            'start': {
                'dateTime': startTimeString,
            },
            'end': {
                'dateTime': endTimeString,

            },

            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': self.setUp},
                ],
            },
        }

        print event
        apiHandler.google.service.events().insert(calendarId=calendarID, body=event).execute()

    def __str__(self):
        return "Name: {}, Length: {}".format(self.title, self.length)