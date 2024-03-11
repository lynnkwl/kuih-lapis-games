from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

import datetime

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%m-%d %H:%M")
print("Current Date and Time:", formatted_datetime)

subject = "Your order was shipped on " + formatted_datetime
msg = "Dear customer. Your order has been shipped. Please reply to this email if you have any queries."
sender = "kuehgames@email.com"
receiver = "josh@gmail.com"

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
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
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)
message = MIMEText(msg)
message['to'] = receiver
message['from'] = sender
message['subject'] = subject
raw = base64.urlsafe_b64encode(message.as_bytes())
raw = raw.decode()
body = {'raw' : raw}
message = (service.users().messages().send(userId='me', body=body).execute())