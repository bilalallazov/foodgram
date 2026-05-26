from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email', max_length=254, unique=True)
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
