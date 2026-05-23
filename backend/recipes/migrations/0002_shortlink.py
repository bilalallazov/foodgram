from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLink',
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
                ('code', models.SlugField(max_length=16, unique=True)),
                (
                    'recipe',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='short_link',
                        to='recipes.recipe',
                    ),
                ),
            ],
            options={
                'verbose_name': 'short link',
                'verbose_name_plural': 'short links',
            },
        ),
    ]
