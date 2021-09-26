import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client
from math import radians, sin, cos, sqrt, asin


def mailer(template, data, subject, receiver_email, title= "Proxy pharma"):
    from_email = title

    #message
    if template:
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def distance(lat1, long1, lat2, long2):
    """
    Calculate the distance between two point
    """

    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km
