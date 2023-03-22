from django import template
register = template.Library()

@register.filter
def index(sequence, position):
    return sequence[position]

@register.filter
def next(some_list, current_index):
    try:
        return some_list[int(current_index) + 1] # access the next element 
    except:
        return ''

@register.filter
def qry(object, value):
    return object.filter(date_jours=value).exists()
    