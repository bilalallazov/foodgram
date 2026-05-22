import base64
import os

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()

IMAGE_BYTES = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42m'
    'P8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
)


class Command(BaseCommand):
    help = 'Load test users and recipes'

    def handle(self, *args, **options):
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@foodgram.ru')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password=admin_password,
                first_name='Admin',
                last_name='Admin',
            )
        test_users = [
            ('chef1', 'chef1@foodgram.ru', 'Chef', 'One'),
            ('chef2', 'chef2@foodgram.ru', 'Chef', 'Two'),
            ('user1', 'user1@foodgram.ru', 'User', 'One'),
        ]
        for username, email, first_name, last_name in test_users:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123',
                    first_name=first_name,
                    last_name=last_name,
                )
        tags = list(Tag.objects.all()[:2])
        ingredients = list(Ingredient.objects.all()[:5])
        if not tags or len(ingredients) < 2:
            self.stdout.write(
                self.style.WARNING(
                    'Run load_ingredients and create_tags first.'
                )
            )
            return
        chefs = User.objects.filter(username__in=('chef1', 'chef2'))
        for index, chef in enumerate(chefs):
            if Recipe.objects.filter(author=chef).exists():
                continue
            recipe = Recipe(
                author=chef,
                name=f'Тестовый рецепт {index + 1}',
                text='Описание тестового рецепта.',
                cooking_time=30 + index * 10,
            )
            recipe.image.save(
                f'recipe_{chef.username}.png',
                ContentFile(IMAGE_BYTES),
                save=False,
            )
            recipe.save()
            recipe.tags.set(tags)
            for ingredient in ingredients[:3]:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=100 + index * 10,
                )
        self.stdout.write(
            self.style.SUCCESS('Test data loaded successfully.')
        )
