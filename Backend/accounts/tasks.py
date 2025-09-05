from django.utils import timezone
from celery import shared_task
from .utils import send_welcome_email
import time

@shared_task
def send_email(email):
    time.sleep(5)
    print(f"send to {email} ")
    return f" email sent to {email}"




@shared_task

def send_welcome_email_task(fname,lname,email):
    context={
        "first_name":fname,
        "last_name":lname,
        "current year":timezone.now().year


    }
    try:
        send_welcome_email(
            subject="Welcome to ngererayo platform",
            context=context,
            to_email=email,
            template_name="accounts/welcome_email.html"
        )
    except Exception as e:
         return f"Error sending email: {str(e)}"