from .celery import app
from apps.account.send_email import send_confirmation_email


@app.task
def send_confirmation_email_task(user, code):
    send_confirmation_email(user, code)

