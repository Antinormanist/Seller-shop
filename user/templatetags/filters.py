from django import template

register = template.Library()

@register.filter(name='avg_rate')
def avg_rate(value, arg):
    return round(value / arg, 1)