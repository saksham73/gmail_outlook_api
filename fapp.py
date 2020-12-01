from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json,requests,subprocess as sub
import sys

from flask import Flask,render_template,request,json,session
app=Flask(__name__)

from O365 import Account, FileSystemTokenBackend, MSGraphProtocol
credentials =  ('ba22b1b7-6aa4-42a8-9210-cece4c241534', 'FSu=zr8ds_eeWduq/d[aerK6RLlCDK65')
import pytz

@app.route("/",methods=['GET','POST'])
def view_page():
    return render_template('index.html')

@app.route("/googleauth",methods=['GET','POST'])
def auth_google():
    if request.method == 'POST':
        data=request.json
        print(data['enableAutoReply'])
        autrep=data['enableAutoReply']
        sub=data['responseSubject']
        message=data['responseBodyHtml']
        start=data['startTime']
        end=data['endTime']
        r=functionpost(autrep,sub,message,start,end)
        print(r)
        return render_template('success.html')
    else:
        r=function()
        print(r)
        return r
    
    #r=function()
    #if(r['reply']==False):
        #return r
    #return r

@app.route("/microauth",methods=['GET','POST'])
def auth_micro():
    if request.method == 'POST':
        data=request.json
        r=functionpost_microsoft(data)
        print(r)

        return render_template('success.html')
    else:
        r=function_microsoft()
        print(r)
        return r    


@app.route("/gmailcal",methods=['GET','POST'])
def set_event():
    if request.method == 'POST':
        data=request.json
        r=setGmailevent(data)
        print(r)
        return r

@app.route("/outlookcal",methods=['GET','POST'])
def set_mevent():
    if request.method == 'POST':
        data=request.json
        r=setMicrosoftevent(data)
        print(r)
        return(r)
    return ''

@app.route("/putinterminal",methods=['GET','POST'])
def finish():
    if request.method == 'POST':
        data=request.json
        r=data['val']
        #print(r)
        sys.stderr.write(r)
        return(r)

def function():
        # If modifying these scopes, delete the file token.pickle.  
    SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

    creds = None
    # file="token_adi"
    token_file="token.pickle"
    print(token_file)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    print(service)
    ud='me'
    print(ud)
    

    events_result = service.users().settings().getVacation(userId=ud).execute()


    return(events_result)

def functionpost(autrep,subject,message,start,end):
        # If modifying these scopes, delete the file token.pickle.  
    SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

    creds = None
    # file="token_adi"
    token_file="token.pickle"
    print(token_file)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    ud='me'
    data={
        'enableAutoReply' : autrep,
        'responseSubject': subject,
        'responseBodyHtml': message,
        "startTime": start,
        "endTime": end
    }
    
    print(data['enableAutoReply'])
    try:
       events_result = service.users().settings().updateVacation(userId=ud,body= data).execute()
    except:
        return {'reply':False}

    return(events_result)


def function_microsoft():
    try:
        scopes=['https://graph.microsoft.com/MailboxSettings.Read', 'https://graph.microsoft.com/MailboxSettings.ReadWrite', 'https://graph.microsoft.com/User.Read']  # you can use scope helpers here (see Permissions and Scopes section)
        token_backend = FileSystemTokenBackend(token_path='', token_filename='my_token.txt')
        #protocol = MSGraphProtocol(api_version='v1.0')
        account = Account(credentials, token_backend=token_backend)
        if not account.is_authenticated:
            account.authenticate(scopes=scopes)
        
        with open('my_token.txt', 'r') as myfile:
            data=myfile.read()

        obj = json.loads(data)

        access_token=obj['access_token']
        
        headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

        api_url = 'https://graph.microsoft.com/v1.0/me/mailboxSettings'

        response = requests.get(api_url, headers=headers)

        info=json.loads(response.content.decode('utf-8'))

        return(info['automaticRepliesSetting'])
    except:
        return {'reply': False}


def functionpost_microsoft(data):
    try:
        scopes=['https://graph.microsoft.com/MailboxSettings.Read', 'https://graph.microsoft.com/MailboxSettings.ReadWrite', 'https://graph.microsoft.com/User.Read']  # you can use scope helpers here (see Permissions and Scopes section)
        token_backend = FileSystemTokenBackend(token_path='', token_filename='my_token.txt')
        #protocol = MSGraphProtocol(api_version='v1.0')
        account = Account(credentials, token_backend=token_backend)
        if not account.is_authenticated:
            account.authenticate(scopes=scopes)
        
        with open('my_token.txt', 'r') as myfile:
            tok=myfile.read()

        obj = json.loads(tok)

        access_token=obj['access_token']
        
        headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

        api_url = 'https://graph.microsoft.com/v1.0/me/mailboxSettings'

        info={
            "automaticRepliesSetting": data
        }

        print('info is:::::')
        print(info)

        response = requests.patch(api_url, headers=headers, json=info)

        if response.status_code >= 500:
            print('[!] [{0}] Server Error'.format(response.status_code))
        elif response.status_code == 404:
            print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
        elif response.status_code == 401:
            print('[!] [{0}] Authentication Failed'.format(response.status_code))
        elif response.status_code >= 400:
            print('[!] [{0}] Bad Request'.format(response.status_code))
            print(info)
            print(response.content)
        elif response.status_code >= 300:
            print('[!] [{0}] Unexpected redirect.'.format(response.status_code))
        elif response.status_code == 200:
            posted_content = json.loads(response.content)
            return(posted_content)
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))

    except:
        return {'reply': False}

def setGmailevent(data):

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    token_file="tokencal.pickle"
    print(token_file)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    event = data
    event = service.events().insert(calendarId='primary', body=event).execute()
    return(event)


def setMicrosoftevent(data):
    try:
        scopes=['https://graph.microsoft.com/Calendars.ReadWrite']  # you can use scope helpers here (see Permissions and Scopes section)
        token_backend = FileSystemTokenBackend(token_path='', token_filename='my_tokencal.txt')
        #protocol = MSGraphProtocol(api_version='v1.0')
        account = Account(credentials, token_backend=token_backend)
        if not account.is_authenticated:
            account.authenticate(scopes=scopes)
        
        with open('my_tokencal.txt', 'r') as myfile:
            tok=myfile.read()

        obj = json.loads(tok)

        access_token=obj['access_token']
        
        headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(access_token)}

        api_url = 'https://graph.microsoft.com/v1.0/me/events'

        info = data

        response = requests.post(api_url, headers=headers, json=info)

        if response.status_code >= 500:
            return('[!] [{0}] Server Error'.format(response.status_code))
        elif response.status_code == 404:
            return('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
        elif response.status_code == 401:
            return('[!] [{0}] Authentication Failed'.format(response.status_code))
        elif response.status_code >= 400:
            print('[!] [{0}] Bad Request'.format(response.status_code))
            print(info)
            return(response.content)
        elif response.status_code >= 300:
            return('[!] [{0}] Unexpected redirect.'.format(response.status_code))
        elif response.status_code == 201:
            posted_content = json.loads(response.content)
            return(posted_content)
        else:
            return('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))

    except:
        return {'reply': False}


if __name__ == '__main__':
    app.run(debug=True)

