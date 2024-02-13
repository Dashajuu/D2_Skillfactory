from django import template

register = template.Library()

CENSOR_WORDS = [
    'Apple',
    'рейтинг',
]


@register.filter()
def censor(value):
    if isinstance(value, str):
        for i in CENSOR_WORDS:
            value = value.replace(i[1:], '*' * len(i[1:]))
        return value
    else:
        raise ValueError('Переменная не строкового типа сорри')
