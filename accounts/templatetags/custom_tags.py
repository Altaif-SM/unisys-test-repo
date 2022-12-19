from django import template
from masters.views import RegisteredPrerequisiteCourses,ProgramFeeDetails,ReferralFeeDetails
from payments.models import ProgramRegistrationFeeDetails
from tanseeq_app.models import ApplicationDetails, SecondaryCertificateInfo
from student.models import ProgressMeetingStatus
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
def get_paid_program_amount(application_obj):
    if ProgramFeeDetails.objects.filter(university_id=application_obj.university.id, program_id=application_obj.program.id).exists():
        payment_obj = ProgramFeeDetails.objects.get(university_id=application_obj.university.id, program_id=application_obj.program.id)
        return float(payment_obj.total_amount)
    else:
        return '-'


@register.filter
def get_referral_Fee(application_obj):
    if ReferralFeeDetails.objects.filter(university_id=application_obj.university.id, program_id=application_obj.program.id).exists():
        referral_fee_obj = ReferralFeeDetails.objects.get(university_id=application_obj.university.id, program_id=application_obj.program.id)
        return float(referral_fee_obj.amount)
    else:
        return '-'


@register.filter
def get_application_date(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.created_on.date())
    except:
        return None

@register.filter
def get_application_id(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.tanseeq_id)
    except:
        return None

@register.filter
def get_secondary_certificate(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        secondar_certificate_obj = SecondaryCertificateInfo.objects.get(application_id = app_details_obj.id)
        return str(secondar_certificate_obj.secondary_certificate.school_certificate)
    except:
        return None

@register.filter
def get_seat_number(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        secondar_certificate_obj = SecondaryCertificateInfo.objects.get(application_id = app_details_obj.id)
        return str(secondar_certificate_obj.seat_number)
    except:
        return None

@register.filter
def get_average(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        secondar_certificate_obj = SecondaryCertificateInfo.objects.get(application_id = app_details_obj.id)
        return str(secondar_certificate_obj.average)
    except:
        return None

@register.filter
def get_graduation_year(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        secondar_certificate_obj = SecondaryCertificateInfo.objects.get(application_id = app_details_obj.id)
        return str(secondar_certificate_obj.academic_year.year_name)
    except:
        return None

@register.filter
def get_secondary_city(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        secondar_certificate_obj = SecondaryCertificateInfo.objects.get(application_id = app_details_obj.id)
        return str(secondar_certificate_obj.city.city)
    except:
        return None

@register.filter
def get_applicant_gender(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.gender_type)
    except:
        return None

@register.filter
def get_birth_place(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.country.country_name)
    except:
        return None

@register.filter
def get_birth_date(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.birth_date)
    except:
        return None

@register.filter
def get_mobile_number(user_obj):
    try:
        app_details_obj = ApplicationDetails.objects.get(user_id = user_obj.id)
        return str(app_details_obj.contact_number)
    except:
        return None

@register.filter
def get_progress_meeting_status(progress_obj):
    try:
        progress_meeting_status = ProgressMeetingStatus.objects.get(meeting = progress_obj)
        return str(progress_meeting_status.status)
    except:
        return 'Pending'