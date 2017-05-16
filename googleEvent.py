from utils import *
import datetime
class googleEvent:
    def __init__(self,event):
        self.event = event
        self.start = utc_to_datetime(event["start"]["dateTime"])
        self.end = utc_to_datetime(event["end"]["dateTime"])
        self.duration = self.end-self.start
        if not event["reminders"]["useDefault"]:
            self.start -= datetime.timedelta(minutes=event["reminders"]["overrides"][0]["minutes"])

    def __str__(self):
        string = "eventName:{}, start:{}, end:{}, duration:{}".format(self.event["summary"],\
                                                          self.start.strftime("%b %d, %Y. %H:%M:%S"),\
                                                          self.end.strftime("%b %d, %Y. %H:%M:%S"),\
                                                                      self.duration)

        return string