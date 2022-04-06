from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = {
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
    (USER, 'user'),
}


class UserProfile(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=12,
        blank=True,
        editable=False,
        null=True,
        unique=True
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR
