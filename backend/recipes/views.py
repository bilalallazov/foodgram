from django.shortcuts import get_object_or_404, redirect

from recipes.models import ShortLink


def short_link_redirect(request, code):
    short_link = get_object_or_404(ShortLink, code=code)
    return redirect(f'/recipes/{short_link.recipe_id}')
