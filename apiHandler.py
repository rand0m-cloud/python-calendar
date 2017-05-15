from utils import *
from server import getWunderAccess
import requests

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

        self.headers = {
            "X-Access-Token":self.token,
            "X-Client-ID":self.oauth["client_id"]
        }


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


    def request(self,method,url,data=None):
        request = None

        if method == "GET":
            request = requests.request(method,url,params=data,headers=self.headers)
        else:
            request = requests.request(method,url,data=data,headers=self.headers)

        return self.handleResponse(request)


    def handleResponse(self,req):
        if req.status_code != 200:
            self.genCreds()
            print "Request returned:{}".format(req.status_code)
            raise RuntimeError("Request:{},{},{}",req.url,req.headers,req.text)
            return None

        jsonObj = json.loads(req.text)
        return jsonObj


class apiHandler:
    google = google()
    wunder = wunder()
