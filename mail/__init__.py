from flask import current_app

# Wariant 1 - Flask-Mail
# from flask_mail import Mail, Message, Attachment

# mail = Mail()


# def sendEmail(recipients, subject, body):
#     msg = Message(
#         sender=current_app.config['MAIL_USERNAME'],
#         subject=subject,
#         recipients=recipients,
#         body=body
#     )
#     mail.send(msg)


# Wariant 2 - GMAIL
import os
import pickle

from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from base64 import urlsafe_b64encode

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SCOPES = ['https://mail.google.com/']


def gmail_authenticate():
    __tokenFile = current_app.config['GMAIL_TOKEN']
    creds = None

    if os.path.exists(__tokenFile):
        with open(__tokenFile, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return build('gmail', 'v1', credentials=creds)


def __add_attachment(message, filename):
    pass


def __build_message(destination, obj, body, attachments=None):
    __gMailFrom = current_app.config['GMAIL_FROM']
    if attachments is None:
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = __gMailFrom
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = __gMailFrom
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            __add_attachment(message, filename)

    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def __send_message(service, destination, obj, body, attachments=None):
    return service.users().messages().send(
        userId="me",
        body=__build_message(destination, obj, body, attachments)
    ).execute()


def sendEmail(recipients, subject, body):
    __mail = gmail_authenticate()
    for __to in recipients:
        return __send_message(__mail, __to, subject, body)
