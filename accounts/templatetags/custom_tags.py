from django import template
from masters.views import RegisteredPrerequisiteCourses
register = template.Library()


@register.filter
def is_prerequisite_course_registred(course_id):
    if RegisteredPrerequisiteCourses.objects.filter(course_id = course_id).exists():
        return True
    else:
        return False

@register.filter
def is_prerequisite_course_user(user):
    if RegisteredPrerequisiteCourses.objects.filter(application_id = user.get_application).exists():
        return True
    else:
        return False


@register.filter
def get_file_name(path):
    try:
        file_name = path.split('document/')
        return file_name[1]
    except:
        return ''

