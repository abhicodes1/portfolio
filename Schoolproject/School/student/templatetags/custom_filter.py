from django import template
register = template.Library()
######filters ##########
@register.filter()
def sub(value, arg):
    return int(value) - int(arg)

@register.filter()
def mul(value, arg):
    return int(value) * int(arg)

@register.filter()
def div(value, arg):
    return int(value) / int(arg)

@register.simple_tag
def go_to_url(url):
    return "window.location='" + url +"'; return false;"

    