from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def incr(x,i):
    x = int(x)
    x+=1
    return x