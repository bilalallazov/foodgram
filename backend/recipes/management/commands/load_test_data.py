import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()

RECIPE_COUNT = 7
PLACEHOLDER_SIZE = (600, 400)
PLACEHOLDER_COLORS = (
    (255, 214, 165),
    (255, 183, 178),
    (198, 226, 191),
    (197, 217, 232),
    (230, 210, 240),
    (255, 236, 179),
    (188, 223, 197),
)


def build_placeholder_image(index):
    color = PLACEHOLDER_COLORS[index % len(PLACEHOLDER_COLORS)]
    image = Image.new('RGB', PLACEHOLDER_SIZE, color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=90)
    return buffer.getvalue()


def recipe_needs_image(recipe):
    if not recipe.image or not recipe.image.name:
        return True
    try:
        return recipe.image.size < 500
    except (OSError, ValueError):
        return True


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
        tags = list(Tag.objects.all())
        ingredients = list(Ingredient.objects.all()[:5])
        if len(tags) < 3 or len(ingredients) < 2:
            self.stdout.write(
                self.style.WARNING(
                    'Run load_ingredients and create_tags first.'
                )
            )
            return
        authors = list(
            User.objects.filter(
                username__in=('admin', 'chef1', 'chef2', 'user1')
            )
        )
        if not authors:
            return

        existing_count = Recipe.objects.count()
        if existing_count < RECIPE_COUNT:
            for index in range(existing_count, RECIPE_COUNT):
                author = authors[index % len(authors)]
                recipe = Recipe(
                    author=author,
                    name=f'Тестовый рецепт {index + 1}',
                    text='Описание тестового рецепта.',
                    cooking_time=30 + index * 5,
                )
                recipe.image.save(
                    f'recipe_{index + 1}.jpg',
                    ContentFile(build_placeholder_image(index)),
                    save=False,
                )
                recipe.save()
                recipe.tags.set([tags[index % len(tags)]])
                for ingredient in ingredients[:3]:
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=100 + index * 10,
                    )

        fixed_images = 0
        for index, recipe in enumerate(Recipe.objects.order_by('id')):
            if recipe_needs_image(recipe):
                recipe.image.save(
                    f'recipe_{recipe.id}.jpg',
                    ContentFile(build_placeholder_image(index)),
                    save=True,
                )
                fixed_images += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Test data ready: {Recipe.objects.count()} recipes, '
                f'fixed images: {fixed_images}.'
            )
        )
