import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('recipes', '0003_remove_subscription'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Subscription',
                    fields=[
                        (
                            'id',
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name='ID',
                            ),
                        ),
                        (
                            'author',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name='subscribers',
                                to=settings.AUTH_USER_MODEL,
                                verbose_name='author',
                            ),
                        ),
                        (
                            'user',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name='subscriptions',
                                to=settings.AUTH_USER_MODEL,
                                verbose_name='subscriber',
                            ),
                        ),
                    ],
                    options={
                        'verbose_name': 'subscription',
                        'verbose_name_plural': 'subscriptions',
                        'db_table': 'recipes_subscription',
                    },
                ),
                migrations.AddConstraint(
                    model_name='subscription',
                    constraint=models.UniqueConstraint(
                        fields=('user', 'author'),
                        name='unique_subscription',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
