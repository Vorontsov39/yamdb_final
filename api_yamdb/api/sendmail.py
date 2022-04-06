from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_SUPPORT
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def mail(profile):
    code = PasswordResetTokenGenerator()
    send_mail(
        'Код подтверждения',
        f'{code}',
        EMAIL_SUPPORT,
        [f'{profile.email}'],
        fail_silently=False
    )
    return code
