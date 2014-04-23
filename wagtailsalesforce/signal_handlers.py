from django.dispatch.dispatcher import receiver
from wagtail.wagtaildocs.models import Document, doc_serve
from django.contrib.auth.signals import user_logged_in

from .salesforce import get_salesforce


def log_doc_serve(sender, request, **kwargs):
    sf = get_salesforce()
    sf.log_doc_serve(sender)


def log_user_logged_in(sender, user, request, **kwargs):
    sf = get_salesforce()
    sf.log_user_logged_in(user)


def register_signal_handlers():
    doc_serve.connect(log_doc_serve)
    user_logged_in.connect(log_user_logged_in)
