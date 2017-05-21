import datetime

from utils import *
from server import getWunderAccess
import requests

from utils import getInputFromList


class google:

    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)


class wunder:

    def genCreds(self):
        if os.path.isfile("wunderaccess.json"):
            os.remove("wunderaccess.json")

        self.token = getWunderAccess(self.oauth)

        with open("wunderaccess.json", "w") as wunderaccess:
            obj = {
                "access_token": self.token
            }
            wunderaccess.write(json.dumps(obj))

    def __init__(self):
        with open("wunderoauth.json", "r") as wunderoauth:
            self.oauth = json.load(wunderoauth)

        if os.path.isfile("wunderaccess.json"):
            with open("wunderaccess.json") as wunderaccess:
                self.token = json.load(wunderaccess)["access_token"]
        else:
            self.genCreds()

        self.headers = {
            "X-Access-Token": self.token,
            "X-Client-ID": self.oauth["client_id"]
        }

        self.headers2 = {
            "X-Access-Token": self.token,
            "X-Client-ID": self.oauth["client_id"],
            "Content-Type":"text/json"
        }

    def request(self,method,url,data=None):
        request = None

        if method == "GET" or method == "DELETE":
            request = requests.request(method,url,params=data,headers=self.headers)
        else:
            request = requests.request(method,url, data=json.dumps(data),headers=self.headers2)

        return self.handleResponse(request)


    def handleResponse(self,req):
        if req.status_code != 200 and req.status_code != 204:
            self.genCreds()
            print "Request returned:{}".format(req.status_code)
            raise RuntimeError(req.url,req.text,req.headers)
            return None

        jsonObj = json.loads(req.text)
        return jsonObj


class apiHandler:
    google = google()
    wunder = wunder()


def get_events(calendar_id,minTime=None,maxTime=None):
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
    results = apiHandler.google.service.events().list(calendarId=calendar_id,timeMin=minTime, orderBy="startTime", singleEvents=True).execute()
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