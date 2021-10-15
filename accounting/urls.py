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

                  path('get_payment_report/', views.get_payment_report, name='get_payment_report'),
                  path('get_repayment_report/', views.get_repayment_report, name='get_repayment_report'),
                  path('get_filtered_student_report/', views.get_filtered_student_report, name='get_filtered_student_report'),

                  path('get_approval_and_paid_total/', views.get_approval_and_paid_total, name='get_approval_and_paid_total'),

                  path('get_donor_receipt_voucher/', views.get_donor_receipt_voucher, name='get_donor_receipt_voucher'),
                  path('get_donors_student_list/', views.get_donors_student_list, name='get_donors_student_list'),


                  path('get_payment_voucher_data_by_student/', views.get_payment_voucher_data_by_student, name='get_payment_voucher_data_by_student'),
                  path('get_receipt_voucher_data_by_student/', views.get_receipt_voucher_data_by_student, name='get_receipt_voucher_data_by_student'),


                  path('save_payment_voucher_data_by_student/', views.save_payment_voucher_data_by_student, name='save_payment_voucher_data_by_student'),
                  path('save_student_receipt_voucher/', views.save_student_receipt_voucher, name='save_student_receipt_voucher'),

                  path('get_donor_recipt_for_org_payment/', views.get_donor_recipt_for_org_payment, name='get_donor_recipt_for_org_payment'),
                  path('save_donor_recipt_for_org_payment/', views.save_donor_recipt_for_org_payment, name='save_donor_recipt_for_org_payment'),

                  path('get_donor_report/', views.get_donor_report, name='get_donor_report'),
                  path('get_voucher_data_by_donor/', views.get_voucher_data_by_donor, name='get_voucher_data_by_donor'),
                  path('export_student_recipt_voucher/', views.export_student_recipt_voucher, name='export_student_recipt_voucher'),
                  path('export_student_payment_voucher/', views.export_student_payment_voucher, name='export_student_payment_voucher'),
                  path('export_donor_receipt_report/', views.export_donor_receipt_report, name='export_donor_receipt_report'),
                  path('export_student_receipt_payment_report/', views.export_student_receipt_payment_report, name='export_student_receipt_payment_report'),
                  path('student_receipt_payment_report_export/', views.student_receipt_payment_report_export, name='student_receipt_payment_report_export'),
                  path('export_payment_receipt_report/', views.export_payment_receipt_report, name='export_payment_receipt_report'),

                  path('update_student_payment_voucher/', views.update_student_payment_voucher, name='update_student_payment_voucher'),
                  path('delete_student_payment_voucher/', views.delete_student_payment_voucher, name='delete_student_payment_voucher'),
                  path('update_donar_receipt_voucher/', views.update_donar_receipt_voucher, name='update_donar_receipt_voucher'),
                  path('delete_donar_receipt_voucher/', views.delete_donar_receipt_voucher, name='delete_donar_receipt_voucher'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
