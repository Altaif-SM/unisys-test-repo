from django.urls import path, include
from rest_framework import routers
from rest_api import views
app_name = 'rest_api'

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('payment_refund_complete/', views.PaymentRefundCompleteView.as_view(), name="payment_refund_complete"),

]
