from django import template

register = template.Library()

@register.filter(name='to_currency')
def to_currency(value):
    """
    強制將數字轉換為千分位格式
    用法: {{ value|to_currency }}
    """
    try:
        value = int(float(value))
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value