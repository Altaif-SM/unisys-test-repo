from django.http.request import QueryDict
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.contrib import messages
from tanseeq_app.models import (
    AppliedPrograms,
)


class AdvanceOrders(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_finance/list_applied_students.html"

    def get_queryset(self):
        filter_by_fee = self.request.GET.get("filter_by_fee")
        filters={}
        if filter_by_fee == "paid":
            filters["bond_no__isnull"] = False
        elif filter_by_fee == "un paid":
            filters["bond_no__isnull"] = True
        return self.model.objects.filter(is_denied=False, **filters).select_related("program_details")
        


class ManageAdvanceOrders(View):
    model = AppliedPrograms

    def patch(self, request, pk):
        print("POST", request.POST)
        print("body",request.body)
        data = QueryDict(request.body)
        print("data: =",data)
        bond_no = data.get("bond_no")
        if not bond_no:
            return JsonResponse({"msg": "Bond No. is required."}, status=304)
        obj = self.model.objects.filter(pk=pk)
        if not obj:
            return JsonResponse({}, status=404)
        obj.update(bond_no=bond_no)
        return JsonResponse({}, status=200)
    
    def delete(self, request, pk):
        obj = self.model.objects.filter(pk=pk)
        if not obj:
            return JsonResponse(status=404)
        obj.update(is_denied=True)
        return JsonResponse({}, status=200)
