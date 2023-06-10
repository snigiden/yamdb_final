from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLE_CHOICES = [
    ('anonimous', 'anonimous'),
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Никнейм',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    role = models.TextField(
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        null=True,
    )
    first_name = models.TextField(
        null=True,
        max_length=150,
    )
    last_name = models.TextField(
        null=True,
        max_length=150,
    )
    confirmation_code = models.CharField(
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['first_name', ], name='user_first_name_idx'),
            models.Index(fields=['last_name', ], name='user_last_name_idx'),
        ]

    @property
    def is_user(self):
        return self.role == ROLE_CHOICES[1][0]

    @property
    def is_moderator(self):
        return self.role == ROLE_CHOICES[2][0]

    @property
    def is_admin(self):
        return (
            self.role == ROLE_CHOICES[3][0]
            or self.is_superuser
        )
