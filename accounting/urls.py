from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'accounting'

urlpatterns = [
                  path('get_student_payment_voucher/', views.get_student_payment_voucher, name='get_student_payment_voucher'),
                  path('get_student_receipt_voucher/', views.get_student_receipt_voucher, name='get_student_receipt_voucher'),
                  path('get_student_payment_and_receipt_report/', views.get_student_payment_and_receipt_report, name='get_student_payment_and_receipt_report'),
                  path('get_student_report/', views.get_student_report, name='get_student_report'),
                  path('get_approval_and_paid_total/', views.get_approval_and_paid_total, name='get_approval_and_paid_total'),
                  path('get_donor_receipt_voucher/', views.get_donor_receipt_voucher, name='get_donor_receipt_voucher'),
                  path('get_donor_report/', views.get_donor_report, name='get_donor_report'),

                  path('get_payment_voucher_data_by_student/', views.get_payment_voucher_data_by_student, name='get_payment_voucher_data_by_student'),
                  path('save_payment_voucher_data_by_student/', views.save_payment_voucher_data_by_student, name='save_payment_voucher_data_by_student'),
                  path('save_student_receipt_voucher/', views.save_student_receipt_voucher, name='save_student_receipt_voucher'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
