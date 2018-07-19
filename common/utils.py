import random
import string
from masters.models import YearDetails
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.contrib import messages


def random_string_generator(size, include_lowercase=True, include_uppercase=True, include_number=True):
    s = ""
    if include_lowercase:
        s = s + string.ascii_lowercase
    if include_uppercase:
        s = s + string.ascii_uppercase
    if include_number:
        s = s + string.digits

    if len(s) > 0:
        s = ''.join(random.sample(s, len(s)))
        return ''.join(random.choice(s) for _ in range(size))


def handle_uploaded_file(url, file):
    with open(str(url), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def get_application_id(application_obj):
    current_year = YearDetails.objects.get(active_year=True)
    year_name = ''.join(current_year.year_name.split(' '))

    application_id = year_name + '-' + str(application_obj.id)
    return application_id


def send_email_to_applicant(from_email, to_mail, subject, message, first_name):
    # from_email = settings.EMAIL_HOST_USER
    to = [to_mail, from_email]

    template = get_template('mail_template_approving_student_application.html')
    html_content = render_to_string('mail_template_approving_student_application.html',
                                    {'first_name': first_name, 'message': message})

    try:
        send_mail(subject, message, from_email, to, fail_silently=True, html_message=html_content)
    except:
        messages.warning('Network Error Occur Please Try Later')
    return to_mail


def create_voucher_number(voucher_type, voucher):
    voucher_number = ""
    if voucher:
        current_year = YearDetails.objects.get(active_year=True)
        year_name = ''.join(current_year.year_name.split(' '))
        voucher_number = str(voucher_type) + "-" + year_name + "-" + str(voucher.id)

    return voucher_number
