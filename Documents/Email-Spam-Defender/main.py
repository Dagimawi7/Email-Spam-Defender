from __future__ import print_function
import os.path
import base64
import email
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying SCOPES, delete token.json
SCOPES = ['https://mail.google.com/']


def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def list_messages(service):
    results = service.users().messages().list(userId='me', q='is:inbox').execute()
    messages = results.get('messages', [])
    return messages

# -------------------------------------------------------------------------
# Helper functions for spam detection / handling

def get_message_detail(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")

    subject = ""
    sender = ""
    for item in headers:
        if item["name"] == "Subject":
            subject = item["value"]
        if item["name"] == "From":
            sender = item["value"]

    parts = payload.get("parts")
    body = ""
    if parts:
        for part in parts:
            data = part.get("body", {}).get("data")
            if data:
                body += base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8")
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8")

    return subject, sender, body

SPAM_KEYWORDS = ["free money", "congratulations", "bitcoin", "sext", "lottery", "claim now"]

def is_spam(subject, body):
    text = (subject + " " + body).lower()
    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            return True
    if re.search(r"\$\d{3,}", text):  # pattern for money like $1000
        return True
    return False

def move_to_spam(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': ['SPAM'], 'removeLabelIds': ['INBOX']}
    ).execute()

def delete_message(service, msg_id):
    service.users().messages().delete(userId='me', id=msg_id).execute()

# -------------------------------------------------------------------------

if __name__ == '__main__':
    service = gmail_authenticate()
    messages = list_messages(service)

    print(f"Scanning {len(messages)} inbox messages...")

    for m in messages:
        msg_id = m['id']
        subject, sender, body = get_message_detail(service, msg_id)

        if is_spam(subject, body):
            print(f"[SPAM] {subject} → moving to spam & deleting")
            move_to_spam(service, msg_id)
            delete_message(service, msg_id)
        else:
            print(f"[OK]   {subject}")
