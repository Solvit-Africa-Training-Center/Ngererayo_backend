from django.core.mail import EmailMessage
from django.template.loader import render_to_string




def send_welcome_email(subject, to_email,context,template_name):
     html_message=render_to_string(template_name,context)
     email=EmailMessage(
          subject=subject,
          body=html_message,
          to=[to_email]
     )
     email.content_subtype='html'
     email.send()
