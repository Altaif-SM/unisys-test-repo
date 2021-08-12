from django import template

register = template.Library()

@register.filter
def get_file_name(path):
    try:
        file_name = path.split('document/')
        return file_name[1]
    except:
        return ''

