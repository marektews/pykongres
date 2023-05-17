from flask import current_app
from flask_mail import Mail, Message, Attachment

mail = Mail()


def sendEmail(recipients, subject, body):
    msg = Message(
        sender=current_app.config['MAIL_USERNAME'],
        subject=subject,
        recipients=recipients,
        body=body
    )
    mail.send(msg)
