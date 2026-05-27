from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator],
        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ '
            'only.'
        ),
    )
    email = models.EmailField(
        'email address',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        default='',
        blank=True,
        null=True,
        verbose_name='avatar',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.username
