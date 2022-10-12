from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    TanseeqUniversityDetails,
    TanseeqCountry,
    TansseqCity,
)
from masters.models import UniversityDetails, YearDetails
from tanseeq_app.forms import (
    TanseeqPeriodForm,
    UniversityDetailsForm,
    SecondarySchoolCertificateForm,
    UniversityAttachmentForm,
    UniversityForm,
    CountryForm,
    CityForm,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


class TanseeqAdminHome(TemplateView):
    template_name = 'tanseeq_admin/admin_home.html'


class UniversityList(ListView):
    model = TanseeqUniversityDetails
    template_name = "tanseeq_admin/list_university.html"


class UniversityView(View):
    model = TanseeqUniversityDetails
    form_class = UniversityForm

    def get(self, request, pk=None):
        context = {
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, "tanseeq_admin/add_university.html", context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, request.FILES, instance=instance)
        else:
            form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_university.html', context)
        return redirect('tanseeq_app:list_university')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        messages.success(request, "Record removed.")
        return JsonResponse({"status": 200})


class UniversityDetailView(View):
    model = TanseeqUniversityDetails

    def get(self, request, pk=None):
        context = {}
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
        return render(request, 'tanseeq_admin/add_university.html', context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = UniversityForm(request.POST, request.FILES, instance=instance)
        else:
            form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if not pk:
                obj.created_by = request.user
            obj.save()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_university.html', context)
        return redirect('tanseeq_app:list_university')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


class TanseeqPeriodListView(ListView):
    model = TanseeqPeriod
    template_name = 'tanseeq_admin/tanseeq_period_view.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset


class TanseeqPeriodView(View):
    model = TanseeqPeriod

    def get(self, request, pk=None):
        context = self.get_context()
        context["is_edit"] = pk
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
        return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)

    @staticmethod
    def get_context():
        university_objs = UniversityDetails.active_records()
        academic_year_objs = YearDetails.active_records()
        return {
            "university_objs": university_objs,
            "academic_year_objs": academic_year_objs,
        }

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
            form = TanseeqPeriodForm(request.POST, instance=instance)
        else:
            form = TanseeqPeriodForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not pk:
                obj.created_by = request.user
                messages.success(request, "Record saved.")
            else:
                messages.success(request, "Record Updated.")
            obj.save()
        else:
            context = self.get_context()
            context['form'] = form
            return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)
        return redirect('tanseeq_app:list_tanseeq_period')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        messages.success(request, "Record removed.")
        return JsonResponse({"status": 200})


class UniversityGuideList(ListView):
    model = UniversityDetails
    template_name = "tanseeq_admin/list_university_guide.html"
    fields = ["university_name", "file"]


class UniversityGuideUpdateView(UpdateView):
    model = UniversityDetails
    template_name = "tanseeq_admin/add_university_guide.html"
    form_class = UniversityDetailsForm

    def post(self, request, *args, **kwargs):
        university_id = request.POST.get("university_id")
        instance = get_object_or_404(self.model, pk=university_id)
        form = self.form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


class UniversityGuideDeleteView(DeleteView):
    model = UniversityDetails

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.file.delete()
        return JsonResponse({"status": 200})


class SecondarySchoolCertificateListView(ListView):
    model = SecondarySchoolCetificate
    template_name = 'tanseeq_admin/secondary_certificate_view.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset

    def post(self, request, pk=None):
        form = SecondarySchoolCertificateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
            return redirect('tanseeq_app:list_secondary_certificate')
        else:
            messages.warning(request, "Record not saved.")
            return redirect('tanseeq_app:list_secondary_certificate')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


class SecondarySchoolCertificateUpdateView(UpdateView):
    model = SecondarySchoolCetificate
    template_name = "tanseeq_admin/secondary_certificate_view.html"
    form_class = SecondarySchoolCertificateForm

    def post(self, request, *args, **kwargs):
        school_certificate_id = request.POST.get("school_certificate_id")
        instance = get_object_or_404(self.model, pk=school_certificate_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


class UniversityAttachmentList(ListView):
    model = UniversityAttachment
    template_name = "tanseeq_admin/list_university_attachment.html"


class UniversityAttachmentView(View):
    model = UniversityAttachment
    form_class = UniversityAttachmentForm

    def get(self, request, pk=None):
        university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, "tanseeq_admin/add_university_attachment.html", context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            context = {
                "university_objs": UniversityDetails.active_records(),
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_university_attachment.html', context)
        return redirect('tanseeq_app:list_university_attachment')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        messages.success(request, "Record removed.")
        return JsonResponse({"status": 200})


class CountryListView(ListView):
    model = TanseeqCountry
    template_name = 'tanseeq_admin/list_country.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset

    def post(self, request, pk=None):
        form = CountryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
            return redirect('tanseeq_app:list_country')
        else:
            context = {
                "form": form,
            }
            return render(request, 'tanseeq_admin/list_country.html', context)

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})

class CountryUpdateView(UpdateView):
    model = TanseeqCountry
    template_name = "tanseeq_admin/list_country.html"
    form_class = CountryForm

    def post(self, request, *args, **kwargs):
        country_id = request.POST.get("country_id")
        instance = get_object_or_404(self.model, pk=country_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


class CityListView(View):
    model = TansseqCity
    form_class = CityForm
    def get(self, request, pk=None):
        city_objs = TanseeqCountry.objects.get(id = pk).cities.all()
        context = {
            "city_objs": city_objs,
            "form": self.form_class(),
            "country_id": pk,
        }
        return render(request, "tanseeq_admin/list_city.html", context)

    def post(self, request, pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            country_obj = TanseeqCountry.objects.get(id=pk)
            city_obj = TansseqCity.objects.create(city=form.data['city'])
            country_obj.cities.add(city_obj)
            messages.success(request, "Record saved.")
        else:
            city_objs = TanseeqCountry.objects.get(id=pk).cities.all()
            context = {
                "city_objs": city_objs,
                "form": form,
            }
            return render(request, 'tanseeq_admin/list_city.html', context)
        return redirect('tanseeq_app:list_country')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


class CityUpdateView(UpdateView):
    model = TansseqCity
    template_name = "tanseeq_admin/list_city.html"
    form_class = CityForm

    def post(self, request, *args, **kwargs):
        city_id = request.POST.get("city_id")
        instance = get_object_or_404(self.model, pk=city_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})

