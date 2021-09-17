from django.shortcuts import render
from django.http import JsonResponse
from masters.views import *
from payments.models import *
# Create your views here.

def checkout(request):
    application_obj = None
    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)
    try:
        payement_obj = PaymentDetails.objects.get()
    except:
        payement_obj = None
    return render(request, 'checkout.html',{'application_obj':application_obj,'payement_obj':payement_obj})


def payment_complete(request):
    try:
        body = json.loads(request.body)
        transaction_id = body['orderData']['purchase_units'][0]['payments']['captures'][0]['id']
        status = body['orderData']['purchase_units'][0]['payments']['captures'][0]['status']
        currency_code = body['orderData']['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
        amount = body['orderData']['purchase_units'][0]['payments']['captures'][0]['amount']['value']
        OrderDetails.objects.create(application_id=request.user.get_application,user = request.user,transaction_id = transaction_id,
                                    status = status,currency_code = currency_code,amount = amount)
        return JsonResponse('Payment completed', safe=False)
    except:
        return JsonResponse('Payment not completed', safe=False)

def order_complete(request, transaction_id):
    print("transaction_id"+str(transaction_id))
    try:
        order_obj = OrderDetails.objects.get(transaction_id = transaction_id)
    except:
        order_obj = None
    return render(request, 'order_complete.html',{'order_obj':order_obj})

def checkout_2(request):
    return render(request,'checkout_2.html')