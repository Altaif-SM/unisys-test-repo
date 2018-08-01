# -*- coding: utf-8 -*-
import random
import string
from masters.models import YearDetails
from student.models import StudentNotifications, AdminNotifications
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, TableStyle, Table
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import xlsxwriter
from io import BytesIO
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


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
        try:
            for id in applicant_id:
                StudentNotifications.objects.create(applicant_id_id=id[0], message=message)
        except:
            pass


def admin_notification(applicant_id, message):
    try:
        AdminNotifications.objects.create(applicant_id_id=applicant_id, message=message)
    except:
        pass


def get_admin_notification():
    try:
        return AdminNotifications.objects.filter(applicant_id__year=get_current_year(), applicant_id__is_submitted=True)
    except:
        pass


def export_pdf(output_file_name, records):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + str(output_file_name) + '.pdf'

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

def export_pdf1():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + str('Helo') + '.pdf'

    elements = []

    doc = SimpleDocTemplate(response, topMargin=20)
    doc.pagesize = landscape(A4)

    # #Get this line right instead of just copying it from the docs
    data = [['00', '01', '02', '03', '04','05'],
            ['10', '11', '12', '13', '14','15'],
            ['20', '21', '22', '23', '24','25'],
            ['30', '31', '32', '33', '34','35'],
            ['40', '41', '42', '43', '44','45']]
    table_obj = Table(data)
    table_obj = Table(data, 6 * [0.4 * inch], 5 * [0.4 * inch])
    table_obj.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                   ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                                   ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                                   ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                   ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                   ]))
    # Configure style and word wrap

    # ps = ParagraphStyle('title', fontSize=10, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10)
    # ps = ParagraphStyle('title', fontSize=10, alignment=TA_RIGHT, spaceBefore=10, spaceAfter=10)

    # s = getSampleStyleSheet()
    # s = s["BodyText"]
    # s.wordWrap = 'LTR'
    # data = [[Paragraph(cell, s) for cell in row] for row in records]
    # table_obj = Table(data)
    # table_obj.setStyle(style)

    elements.append(table_obj)
    doc.build(elements)
    return response


def export_wraped_column_xls(output_file_name, column_names, rows):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(output_file_name)
    unlocked = workbook.add_format({'locked': False, 'text_wrap': True})
    locked = workbook.add_format({'locked': True, 'text_wrap': True})
    worksheet.set_column('A:XDF', None, unlocked)
    row_num = 0
    for col_num in range(len(column_names)):
        worksheet.set_column(col_num, col_num, 18)
        worksheet.write(row_num, col_num, column_names[col_num], unlocked)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), unlocked)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + output_file_name + ".xls"

    return response


def get_current_year():
    try:
        return YearDetails.objects.get(active_year=True)
    except:
        return None


def export_debit_wraped_column_xls(output_file_name, column_names, rows, rec_len, total_balance):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(output_file_name)
    unlocked = workbook.add_format({'locked': False, 'text_wrap': True})
    locked = workbook.add_format({'locked': True, 'text_wrap': True})
    worksheet.set_column('A:XDF', None, unlocked)
    row_num = 0
    for col_num in range(len(column_names)):
        worksheet.set_column(col_num, col_num, 18)
        worksheet.write(row_num, col_num, column_names[col_num], unlocked)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), unlocked)

    start_column = 2
    rec_len = rec_len + 1
    worksheet.write(rec_len, start_column, total_balance)

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + output_file_name + ".xls"

    return response


def export_student_payment_wraped_column_xls(output_file_name, column_names, rows, rec_len, debit_total,
                                             outstanding_total):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(output_file_name)
    unlocked = workbook.add_format({'locked': False, 'text_wrap': True})
    locked = workbook.add_format({'locked': True, 'text_wrap': True})
    worksheet.set_column('A:XDF', None, unlocked)
    row_num = 0
    for col_num in range(len(column_names)):
        worksheet.set_column(col_num, col_num, 18)
        worksheet.write(row_num, col_num, column_names[col_num], unlocked)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), unlocked)

    rec_len = rec_len + 1
    start_column = 4
    worksheet.write(rec_len, start_column, debit_total)

    start_column = 5
    worksheet.write(rec_len, start_column, outstanding_total)

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + output_file_name + ".xls"

    return response


def export_last_row_wraped_column_xls(output_file_name, column_names, rows, rec_len, temp_list):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(output_file_name)
    unlocked = workbook.add_format({'locked': False, 'text_wrap': True})
    locked = workbook.add_format({'locked': True, 'text_wrap': True})
    worksheet.set_column('A:XDF', None, unlocked)
    row_num = 0
    for col_num in range(len(column_names)):
        worksheet.set_column(col_num, col_num, 18)
        worksheet.write(row_num, col_num, column_names[col_num], unlocked)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), unlocked)

    rec_len = rec_len + 1
    start_column = 3
    for i in temp_list:
        worksheet.write(rec_len, start_column, i)
        start_column = start_column + 1

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + output_file_name + ".xls"

    return response


def send_email_with_template(application_obj, context, subject, email_body, request,flag=False):
    try:
        email_template = email_body
        subject = subject
        text_content = ''

        path = "partner/templates/" + str(application_obj.id) + ".html"
        file_name = str(application_obj.id) + ".html"

        open(path, "w").close()
        text_file = open(path, "w")
        text_file.write(email_template)
        text_file.close()

        email_template = get_template(file_name)

        html_content = email_template.render(context)

        if flag:
            msg = EmailMultiAlternatives(subject, text_content, application_obj.user.email, [application_obj.user.email])
        else:
            msg = EmailMultiAlternatives(subject, text_content, request.user.email, [application_obj.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        if os.path.exists(path):
            os.remove(path)
    except:
        pass


def media_path(application_obj):
    object_path = str(application_obj.first_name) + '_' + str(application_obj.id)
    object_path = settings.MEDIA_ROOT + os.path.join('reports/' + str(object_path))
    if not os.path.exists(str(object_path)):
        os.makedirs(object_path)
    return object_path


def base_path(application_obj):
    return str(settings.MEDIA_URL) + str('reports/') + str(application_obj.first_name) + '_' + str(application_obj.id)+ '/'
