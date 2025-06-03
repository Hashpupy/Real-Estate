from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_welcome_email(user):
    subject = 'Welcome to HomeFinder!'
    html_message = render_to_string('emails/welcome.html', {'user': user})
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False
    )

def send_property_viewed_email(property, user):
    subject = f'Your property "{property.title}" was viewed'
    html_message = render_to_string('emails/property_viewed.html', {
        'user': property.owner,
        'property': property,
        'viewer': user
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [property.owner.email],
        html_message=html_message,
        fail_silently=False
    )

def send_payment_confirmation(transaction):
    subject = f'Payment confirmation for {transaction.get_transaction_type_display()}'
    html_message = render_to_string('emails/payment_confirmation.html', {
        'user': transaction.user,
        'transaction': transaction
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [transaction.user.email],
        html_message=html_message,
        fail_silently=False
    )