import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client


def mailer(template, data, subject, receiver_email, title= "Proxy pharma"):
    from_email = title

    #message 
    html_message = render_to_string(template, data)
    message = strip_tags(html_message)
    
    send_mail(
        subject,
        message,
        from_email,
        [receiver_email],
        fail_silently=False,
        html_message= html_message
    )

def send_message(receiver_num, text):
    client = Client(getattr(settings, 'TWILIO_SSID'), getattr(settings, 'TWILIO_TOKEN'))
    message = client.messages.create(
        to= receiver_num,
        from_= "+15703545385",
        body= text
    )
