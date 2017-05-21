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


def get_credentials():
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'client_secrets.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

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

def getYesNo(prompt):
    input = ""
    while not input.startswith('y') and not input.startswith('n'):
        input = str(raw_input(prompt + ' '))
    if input.startswith('y'):
        return True
    return False