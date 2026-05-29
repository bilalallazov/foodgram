from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.relations import PrimaryKeyRelatedField


class IngredientPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    default_error_messages = {
        **PrimaryKeyRelatedField.default_error_messages,
        'does_not_exist': 'Ингредиент не найден.',
    }

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            if 'does_not_exist' in exc.get_codes():
                raise NotFound(self.error_messages['does_not_exist'])
            raise
