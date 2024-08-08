from django.core.mail import EmailMessage

from celery import shared_task


@shared_task
def send_mail(head: str, body: str, sender: str, getters: list[str]):
    """
    Sends an mail to users
    
    head: head of mail
    body: main message of mail
    sender: email that sends mail
    getters: list of email that get mail
    """
    email = EmailMessage(
            head,
            body,
            sender,
            getters
        )
    email.fail_silently = False
    email.send()