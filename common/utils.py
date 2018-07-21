import random
import string
from masters.models import YearDetails
from student.models import StudentNotifications
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, TableStyle, Table
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_RIGHT


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


def application_notification(applicant_id, message):
    try:
        StudentNotifications.objects.create(applicant_id_id=applicant_id, message=message)
    except:
        pass


def export_pdf(output_file_name, records):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + str(output_file_name)+'.pdf'

    elements = []

    doc = SimpleDocTemplate(response, topMargin=10)
    doc.pagesize = landscape(A4)

    # #Get this line right instead of just copying it from the docs
    style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ])

    # Configure style and word wrap

    ps = ParagraphStyle('title', fontSize=10, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10)
    ps = ParagraphStyle('title', fontSize=10, alignment=TA_RIGHT, spaceBefore=10, spaceAfter=10)

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    data = [[Paragraph(cell, s) for cell in row] for row in records]
    table_obj = Table(data)
    table_obj.setStyle(style)

    elements.append(table_obj)
    doc.build(elements)
    return response
