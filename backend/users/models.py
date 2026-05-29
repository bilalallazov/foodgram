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
            f'Required. {USERNAME_MAX_LENGTH} characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
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


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='subscriber',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='author',
    )

    class Meta:
        db_table = 'recipes_subscription'
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.author}'
