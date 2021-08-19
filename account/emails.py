from django.template import Context, context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token


# current_site = get_current_site(request)
def send_confirmation_email(user):
    context={
        'user':user,
        # 'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user['id'])),
        'token':account_activation_token.make_token(user['id'])
    }
    email_subject = 'Active your account'
    email_body = render_to_string('email_message.html', context)
    email = EmailMessage(email_subject, email_body,
    settings.DEFAULT_FROM_EMAIL, [user['mail']],
    
    )
    return email.send(fail_silently=False)