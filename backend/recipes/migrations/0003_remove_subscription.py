from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_shortlink'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Subscription',
                ),
            ],
            database_operations=[],
        ),
    ]
