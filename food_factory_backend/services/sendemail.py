from django.core.mail import send_mail
from django.conf import settings
from logger import LOGGER

def send_email(subject, message, recipient_list, sender=None):
    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL

    try:
        LOGGER.info("Inside send_email! ",recipient_list)
        send_mail(
            subject,
            message,
            sender,
            recipient_list,
            fail_silently=False  
        )
    except Exception as e:
        LOGGER.error(f"Error sending email:{str(e)}")

