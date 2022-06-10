from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('stripe_checkout/', views.StripeCheckoutView.as_view()),
    path('charge/', views.charge, name='charge'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('order_complete/<str:transaction_id>/', views.order_complete, name='order_complete'),
    path('stripe_checkout_success/<str:session_id>/', views.stripe_checkout_success, name='stripe_checkout_success'),




    path('stripe_checkout_view/', views.StripeCheckoutTestView.as_view(),name='stripe_checkout_view'),
    path('create_checkout_session/', views.CreateCheckoutSessionView.as_view(),name='create_checkout_session'),
    path('success/', views.SuccessView.as_view(),name='success'),
    path('cancel/', views.CancelView.as_view(),name='cancel'),

    path('registration_checkout/', views.registration_checkout, name='registration_checkout'),
    path('create_registration_checkout_session/', views.CreateRegistrationCheckoutSessionView.as_view(),name='create_registration_checkout_session'),
    path('stripe_registration_checkout_success/<str:session_id>/', views.stripe_registration_checkout_success, name='stripe_registration_checkout_success'),

    path('credit_course_registration_checkout/<int:credit_id>/', views.credit_course_registration_checkout, name='credit_course_registration_checkout'),
    path('CreditCheckoutSessionView/', views.CreditCheckoutSessionView.as_view(),name='CreditCheckoutSessionView'),
    path('stripe_credit_checkout_success/<int:credit_id>/<str:course_ids>/', views.stripe_credit_checkout_success, name='stripe_credit_checkout_success'),

    path('course_registration_checkout/<int:semester_id>/', views.course_registration_checkout, name='course_registration_checkout'),
    path('course_registration_checkout_session/', views.CourseRegistrationCheckoutSessionView.as_view(),name='course_registration_checkout_session'),
    path('stripe_course_checkout_success/<int:semester_id>/', views.stripe_course_checkout_success, name='stripe_course_checkout_success'),

]