from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import TokenProxy

from users.models import Subscription, User


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'recipes_count',
        'subscribers_count',
        'avatar_preview',
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

    @admin.display(description='recipes')
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='subscribers')
    def subscribers_count(self, obj):
        return obj.subscribers.count()

    @admin.display(description='avatar')
    def avatar_preview(self, obj):
        if not obj.avatar:
            return '-'
        return mark_safe(f'<img src="{obj.avatar.url}" width="50" />')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user__username', 'author__username')
