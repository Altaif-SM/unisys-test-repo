from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout_2/', views.checkout_2, name='checkout_2'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('order_complete/<str:transaction_id>/', views.order_complete, name='order_complete'),
]