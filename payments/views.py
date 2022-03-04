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
        try:
            payement_obj = PaymentDetails.objects.filter()[0]
        except:
            payement_obj = None
        return render(request, 'checkout.html', {'application_obj': application_obj, 'payement_obj': payement_obj})
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
        try:
            payement_obj = PaymentDetails.objects.filter()[0]
        except:
            payement_obj = None
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(payement_obj.amount)*100),
                            'product_data': {
                                'name': 'Online Admission',
                                'images': ['http://51.75.54.229:9092/static/images/university_logo.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=YOUR_DOMAIN + 'payments/checkout/',
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

