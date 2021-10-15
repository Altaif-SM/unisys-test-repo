from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from payments.models import *
# Create your views here.

class PaymentRefundCompleteView(APIView,):
    def post(self,request):
        try:
            refund_data = request.data
            event_type = refund_data['event_type']
            print("event_type>>>>>>>>>>>>>>>>>>>" + str(event_type))
            print("request>>>>>>>>>>>>>>>>>>>" + str(request.data))
            if event_type == 'PAYMENT.CAPTURE.REFUNDED':
                capture_link = refund_data['resource']['links'][1]
                transaction_id = capture_link['href'].split('/')[6]
                if OrderDetails.objects.filter(transaction_id = transaction_id).exists():
                    order_obj = OrderDetails.objects.get(transaction_id=transaction_id)
                    OrderDetails.objects.create(transaction_id = order_obj.transaction_id,currency_code = order_obj.currency_code,amount = order_obj.amount,
                                                user = order_obj.user,application_id=order_obj.application_id,status = 'REFUNDED')
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_200_OK)
