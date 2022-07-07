from django import template
from masters.views import RegisteredPrerequisiteCourses,ProgramFeeDetails
from payments.models import ProgramRegistrationFeeDetails
from datetime import datetime

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

@register.filter
def is_paid_program_registration_payment(application_obj):
    if ProgramRegistrationFeeDetails.objects.filter(application_id=application_obj.id).exists():
        return True
    else:
        return False


@register.filter
def get_payment_student_date(application_obj):
    if ProgramRegistrationFeeDetails.objects.filter(application_id=application_obj.id).exists():
        payment_obj = ProgramRegistrationFeeDetails.objects.get(application_id=application_obj.id)
        return str(payment_obj.created_on.date())
    else:
        return '-'

@register.filter
def get_student_amount(application_obj):
    if ProgramFeeDetails.objects.filter(university_id=application_obj.university.id, program_id=application_obj.program.id).exists():
        payment_obj = ProgramFeeDetails.objects.get(university_id=application_obj.university.id, program_id=application_obj.program.id)
        return str(payment_obj.total_amount)
    else:
        return '-'
