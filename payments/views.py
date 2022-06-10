from django.shortcuts import render
from django.http import JsonResponse
from masters.views import *
from payments.models import *
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def checkout(request):
    try:
        application_obj = request.user.get_application
        if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
            application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)
        payement_obj = None
        if PaymentDetails.objects.filter(university_id = application_obj.university.id).exists():
            payement_obj = PaymentDetails.objects.get(university_id = application_obj.university.id)
        if payement_obj == None:
            return render(request, 'no_university_fee.html',{'application_obj':application_obj})
        order_obj = None
        if ApplicationFeeDetails.objects.filter(application_id=request.user.get_application.id).exists():
            order_obj = ApplicationFeeDetails.objects.get(application_id_id=request.user.get_application.id)
        return render(request, 'checkout.html', {'application_obj': application_obj, 'payement_obj': payement_obj,'order_obj':order_obj})
    except Exception as e:
        messages.warning(request, "Please Fill The Application Form First ... ")
        return redirect("/")



def payment_complete(request):
    try:
        body = json.loads(request.body)
        print("body>>>>>>>" + str(body))
        transaction_id = body['orderData']['purchase_units'][0]['payments']['captures'][0]['id']
        status = body['orderData']['purchase_units'][0]['payments']['captures'][0]['status']
        currency_code = body['orderData']['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
        amount = body['orderData']['purchase_units'][0]['payments']['captures'][0]['amount']['value']
        OrderDetails.objects.create(application_id=request.user.get_application, user=request.user,
                                    transaction_id=transaction_id,
                                    status=status, currency_code=currency_code, amount=amount)
        return JsonResponse('Payment completed', safe=False)
    except:
        return JsonResponse('Payment not completed', safe=False)


def order_complete(request, transaction_id):
    try:
        order_obj = OrderDetails.objects.get(transaction_id=transaction_id)
    except:
        order_obj = None
    return render(request, 'order_complete.html', {'order_obj': order_obj})


class StripeCheckoutView(TemplateView):
    template_name = 'stripe_checkout.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    if request.method == 'POST':
        customer = stripe.Customer.create(
            email=request.POST["stripeEmail"],
            name='Riyaz Sayyed',
            source=request.POST["stripeToken"],
        )
        customer = stripe.Customer.modify(
            customer.id,
            address={"city": "mumbai", "country": "india", "line1": "unr", "line2": "thane", "postal_code": "421005",
                     "state": "maharashtra"},
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=500,
            currency='inr',
            description="Payment"
        )

        return render(request, 'charge.html')



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = settings.SERVER_HOST_NAME
        application_obj = request.user.get_application
        payement_obj = 1000
        if PaymentDetails.objects.filter(university_id=application_obj.university.id).exists():
            payement_obj = PaymentDetails.objects.get(university_id=application_obj.university.id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(payement_obj.amount)*100),
                            'product_data': {
                                'name': 'Online Admission',
                                'images': ['http://unisys.online/static/images/university_logo.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=YOUR_DOMAIN + 'payments/stripe_checkout_success/session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + 'payments/checkout/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return str(e)


class StripeCheckoutTestView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'

def stripe_checkout_success(request, session_id):
    ApplicationFeeDetails.objects.create(application_id=request.user.get_application)
    return redirect('/payments/checkout/')


def registration_checkout(request):
    try:
        application_obj = request.user.get_application
        if not application_obj.is_offer_accepted:
            return render(request, 'no_registration_fee.html',{'application_obj':application_obj})
        is_university = False
        program_fee_obj = ''

        if application_obj.choice_1 == True and application_obj.choice_2 == False and application_obj.choice_3 == False:
            program_id = application_obj.program.id
        elif application_obj.choice_1 == True and application_obj.choice_2 == True and application_obj.choice_3 == False:
            program_id = application_obj.program_2.id
        elif application_obj.choice_1 == True and application_obj.choice_2 == True and application_obj.choice_3 == True:
            program_id = application_obj.program_3.id
        else:
            program_id = application_obj.program.id

        if not ProgramFeeDetails.objects.filter(university_id = application_obj.university.id,program_id = program_id).exists():
            is_university = True
            return render(request, 'no_registration_fee.html',{'application_obj':application_obj,'is_university':is_university})
        else:
            program_fee_obj = ProgramFeeDetails.objects.get(university_id = application_obj.university.id,program_id = program_id)
        order_obj = None
        if ProgramRegistrationFeeDetails.objects.filter(application_id=request.user.get_application.id).exists():
            order_obj = ProgramRegistrationFeeDetails.objects.get(application_id_id=request.user.get_application.id)
        return render(request, 'registration_checkout.html', {'application_obj': application_obj,'order_obj':order_obj,'program_fee_obj':program_fee_obj})
    except Exception as e:
        messages.warning(request, "Please Fill The Application Form First ... ")
        return redirect("/")


class CreateRegistrationCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = settings.SERVER_HOST_NAME
        application_obj = request.user.get_application
        payement_obj = 1000

        if application_obj.choice_1 == True and application_obj.choice_2 == False and application_obj.choice_3 == False:
            program_id = application_obj.program.id
        elif application_obj.choice_1 == True and application_obj.choice_2 == True and application_obj.choice_3 == False:
            program_id = application_obj.program_2.id
        elif application_obj.choice_1 == True and application_obj.choice_2 == True and application_obj.choice_3 == True:
            program_id = application_obj.program_3.id
        else:
            program_id = application_obj.program.id

        if ProgramFeeDetails.objects.filter(university_id=application_obj.university.id,program_id = program_id).exists():
            payement_obj = ProgramFeeDetails.objects.get(university_id=application_obj.university.id,program_id = program_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(payement_obj.total_amount)*100),
                            'product_data': {
                                'name': 'Program Registration Payment',
                                'images': ['http://unisys.online/static/images/university_logo.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=YOUR_DOMAIN + 'payments/stripe_registration_checkout_success/session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + 'payments/registration_checkout/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return str(e)

def stripe_registration_checkout_success(request, session_id):
    application_obj = request.user.get_application
    ProgramRegistrationFeeDetails.objects.create(application_id=request.user.get_application)
    ApplicationDetails.objects.filter(id = application_obj.id).update(is_paid_registration_fee = True)
    return redirect('/payments/registration_checkout/')

def course_registration_checkout(request, semester_id=None):
    try:
        application_obj = request.user.get_application
        semester_fee_obj = ''
        total_amount = 0
        if not SemesterBasedFeeDetails.objects.filter(study_plan_id = semester_id).exists():
            return render(request, 'no_course_registration_fee.html',{'application_obj':application_obj})
        else:
            semester_fee_obj = SemesterBasedFeeDetails.objects.get(study_plan_id = semester_id)
            semester_fee_recs = semester_fee_obj.semester_fee.all()
            for rec in semester_fee_recs:
                total_amount = float(total_amount) + float(rec.amount)

        checkout_page = False
        if CourseFeeDetails.objects.filter(study_plan_id = semester_id).exists():
            checkout_page = True
        return render(request, 'course_registration_checkout.html', {'application_obj': application_obj,
                                                                     'semester_fee_obj':semester_fee_obj,
                                                                     'total_amount':total_amount,
                                                                     'semester_id':semester_id,
                                                                     'checkout_page':checkout_page})
    except Exception as e:
        messages.warning(request, "Please Fill The Application Form First ... ")
        return redirect("/")


class CourseRegistrationCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = settings.SERVER_HOST_NAME
        semester_id = json.loads(request.body)['semester_id']
        total_amount = 0
        semester_fee_obj = SemesterBasedFeeDetails.objects.get(study_plan_id=semester_id)
        semester_fee_recs = semester_fee_obj.semester_fee.all()
        for rec in semester_fee_recs:
            total_amount = float(total_amount) + float(rec.amount)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(total_amount)*100),
                        'product_data': {
                            'name': 'Course Registration Payment',
                            'images': ['http://unisys.online/static/images/university_logo.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='payment',
            # success_url=YOUR_DOMAIN + 'payments/stripe_course_checkout_success/session_id={CHECKOUT_SESSION_ID}',
            success_url=YOUR_DOMAIN + 'payments/stripe_course_checkout_success/' + str(semester_id),
            cancel_url=YOUR_DOMAIN + 'payments/course_registration_checkout/'+str(semester_id),

        )
        try:
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return str(e)



def stripe_course_checkout_success(request,semester_id):
    CourseFeeDetails.objects.create(study_plan_id = semester_id)
    return redirect('/payments/course_registration_checkout/'+str(semester_id))
