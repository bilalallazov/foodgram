import secrets
import string

from django.core.validators import MinValueValidator
from django.db import models

from recipes.constants import (
    INGREDIENT_NAME_MAX_LENGTH,
    INGREDIENT_UNIT_MAX_LENGTH,
    MIN_COOKING_TIME,
    MIN_INGREDIENT_AMOUNT,
    RECIPE_NAME_MAX_LENGTH,
    SHORT_LINK_CODE_LENGTH,
    SHORT_LINK_CODE_MAX_LENGTH,
    TAG_NAME_MAX_LENGTH,
    TAG_SLUG_MAX_LENGTH,
)
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='name',
    )
    slug = models.SlugField(
        max_length=TAG_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='name',
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_UNIT_MAX_LENGTH,
        verbose_name='measurement unit',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author',
    )
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        verbose_name='name',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='image',
    )
    text = models.TextField(verbose_name='text')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_COOKING_TIME)],
        verbose_name='cooking time',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='pub date',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='tags',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.name


class ShortLink(models.Model):
    recipe = models.OneToOneField(
        Recipe,
        on_delete=models.CASCADE,
        related_name='short_link',
        verbose_name='recipe',
    )
    code = models.SlugField(
        max_length=SHORT_LINK_CODE_MAX_LENGTH,
        unique=True,
        verbose_name='code',
    )

    class Meta:
        verbose_name = 'short link'
        verbose_name_plural = 'short links'

    def __str__(self):
        return f'/s/{self.code}/'

    @classmethod
    def generate_unique_code(cls):
        alphabet = string.ascii_letters + string.digits
        while True:
            code = ''.join(
                secrets.choice(alphabet) for _ in range(SHORT_LINK_CODE_LENGTH)
            )
            if not cls.objects.filter(code=code).exists():
                return code


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='ingredient',
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_INGREDIENT_AMOUNT)],
        verbose_name='amount',
    )

    class Meta:
        verbose_name = 'recipe ingredient'
        verbose_name_plural = 'recipe ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='recipe',
    )

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='recipe',
    )

    class Meta:
        verbose_name = 'shopping cart item'
        verbose_name_plural = 'shopping cart'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.recipe}'


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
