__author__ = 'vaibhav'

from django.shortcuts import render ,redirect,render_to_response
from django.db.models import Q
from django.db import connection, transaction
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from accounts.models import User
from common.utils import random_string_generator

class UserService:

    @staticmethod
    @transaction.atomic
    def save(user, generate_password, reset=False):
        password = None
        if not user.id:
            user.is_active = True

        if user.password and not reset:
            password = user.password
            user.password = make_password(user.password)

        else:
            if generate_password:
                password = random_string_generator(6, include_lowercase=False, include_uppercase=True, include_number=True)
                user.password = make_password(password)
            else:
                user.password = make_password(password)
        user.save() #todo if failed check unique on username (handle already exist user)

        return password


    @staticmethod
    @transaction.atomic
    def create_user(user, user_detail_obj, send_message=False, generate_password=False):
        password = UserService.save(user, generate_password, reset=False)
        # print password
        # user_detail_obj.user_id = user.id
        # user_detail_obj.save()
        # StaffDetailsService.save(staff_detail_obj)

        if send_message:
            ctx = {'email': user.email, 'name': user.first_name, 'activation_key': user.first_name,
                   'password': password}
            data = {}
            template = get_template('register_email.html')
            html = template.render(data)
            subject = ' Successful Registration'
            html_content = render_to_string('register_email.html', ctx)
            text_content = "..."
            to = [user.email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, "", from_email, to, fail_silently=True, html_message=html_content)
            ctx['email']
            # return render_to_response('register_success.html/', ctx)

        return user

    @staticmethod
    @transaction.atomic
    def create_parent(user, user_detail_obj,request, send_message=False, generate_password=False):
        password = UserService.save(user, generate_password, reset=False)
        # print password
        # user_detail_obj.user_id = user.id
        # user_detail_obj.save()
        # StaffDetailsService.save(staff_detail_obj)

        if send_message:
            ctx = {'email': user.email, 'name': user.first_name, 'activation_key': user.first_name,
                   'password': password,'loginlink':'http://'+request.META['HTTP_HOST']}
            data = {}
            template = get_template('parent_register_email.html')
            html = template.render(data)
            subject = ' Successful Registration'
            html_content = render_to_string('parent_register_email.html', ctx)
            text_content = "..."
            to = [user.email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, "", from_email, to, fail_silently=True, html_message=html_content)
            ctx['email']
            # return render_to_response('register_success.html/', ctx)

        return user

class StaffDetailsService:
    @staticmethod
    def save(staff_details):
        staff_details.save()

class AddressDetailsService:
    @staticmethod
    def save_address(address):
        address.save()