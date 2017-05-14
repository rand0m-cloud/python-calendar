import arrow,os,datetime
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from utils import *
from server import *
import httplib2
import os

def utc_to_datetime(timestamp):
    return arrow.get(timestamp).datetime

global calendarID
calendarID = "herpes"
global service
service = None
def get_service():
    global service
    if service == None:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
    return service

def get_calendarID():
    global calendarID
    return calendarID

def set_calendarID(poop):
    global calendarID
    calendarID = poop

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getInputFromList(list,names):
    index = 0
    for item in names:
        index += 1
        print "{}:{}".format(index,item)
    while True:
        input = str(raw_input("Select 1-{}\n:".format(index)))
        try:
            num = int(input)
            if num>=1 and num<=index:
                index=num
                break

        except:
            pass
    return list[index-1]