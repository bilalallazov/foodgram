from rest_framework.relations import PrimaryKeyRelatedField


class IngredientPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    default_error_messages = {
        **PrimaryKeyRelatedField.default_error_messages,
        'does_not_exist': 'Ингредиент не найден.',
    }
