from django.core.exceptions import  ValidationError
from django.utils.translation import gettext_lazy as _


def is_seeker(user):
    return user.groups.filter(name='Seeker').exists()

def is_jobless(user):
    return user.groups.filter(name='Jobless').exists()

def is_draft(object):
    if object.published == "False":
        return True
    else: 
        False

def validate_motivation(entry):
    if entry == "Why do you want to work for us?":
        raise ValidationError(
            _('You have not entered a motivation letter!'),
            params={'entry' : entry}
        )