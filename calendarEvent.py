from utils import *
import datetime
class calendarEvent:
    def __init__(self,event):
        self.event = event
        self.start = utc_to_datetime(event["start"]["dateTime"])
        self.end = utc_to_datetime(event["end"]["dateTime"])
        self.duration = self.end-self.start
    def __str__(self):
        string = "eventName:{}, start:{}, end:{}, duration:{}".format(self.event["summary"],\
                                                          self.start.strftime("%b %d, %Y. %H:%M:%S"),\
                                                          self.end.strftime("%b %d, %Y. %H:%M:%S"),\
                                                                      self.duration)

        return string