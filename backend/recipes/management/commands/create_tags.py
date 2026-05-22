from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Create default tags'

    def handle(self, *args, **options):
        tags = [
            ('Завтрак', 'breakfast'),
            ('Обед', 'lunch'),
            ('Ужин', 'dinner'),
        ]
        for name, slug in tags:
            Tag.objects.get_or_create(name=name, slug=slug)
        self.stdout.write(self.style.SUCCESS('Tags created successfully.'))
