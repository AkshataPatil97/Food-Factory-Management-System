from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list, sender=None):
    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            message,
            sender,
            recipient_list,
            fail_silently=False  
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")