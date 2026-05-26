def build_shopping_list_text(ingredients):
    lines = ['Список покупок:', '']
    for index, item in enumerate(ingredients, start=1):
        name = item['ingredient__name']
        unit = item['ingredient__measurement_unit']
        amount = item['amount']
        lines.append(f'{index}. {name} ({unit}) — {amount}')
    return '\n'.join(lines)
