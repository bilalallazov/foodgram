import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from CSV file'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data' / 'ingredients.csv'
        ingredients = []
        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, measurement_unit = row
                ingredients.append(
                    Ingredient(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                )
        Ingredient.objects.bulk_create(
            ingredients,
            ignore_conflicts=True,
        )
        self.stdout.write(
            self.style.SUCCESS('Ingredients loaded successfully.')
        )
