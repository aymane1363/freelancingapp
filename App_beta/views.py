from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from App_beta.forms import CreateForm, CreateProjectForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .filters import ServiceFilter
from .forms import ApplyServiceForm
from datetime import datetime
# Create your views here.

class home(View):
    model = Service
    template_name = "App_beta/home.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            service_list = Service.objects.filter(query).select_related()
        else :
            service_list = Service.objects.all()

        myFilter = ServiceFilter(request.GET, service_list)
        service_list = myFilter.qs
        
        if Freelancer.objects.filter(user=request.user.pk).exists():
            ck=True
        else:
            ck=False
        ctx = {'Services' : service_list, 'search': strval, 'myFilter' : myFilter,'ck':ck}
        return render(request, self.template_name, ctx)
    
def FreelancerHome(request):
    return render(request, 'App_beta/freelancer_home.html')
#Freelancer Space
def FreelancerSpace(request):
    projects=Project.objects.all()
    ctx={'projects':projects}
    return render(request, 'App_beta/freelancer_dashboard.html',ctx)

def FreelancerProposals(request):
    projects=Project.objects.filter(Q(freelancer=None),Q(status=3)).all()
    ctx={'projects':projects}
    return render(request, 'App_beta/freelancer_proposals.html',ctx)

class FreelancerServices(LoginRequiredMixin,View):
    def get(self,request):
        Has_services=Has_service.objects.filter(Q(freelancer=self.request.user.freelancer)).all()
        ctx={'Has_services':Has_services} 
        return render(request, 'App_beta/freelancer_services.html',ctx)

#/Freelance pace
def ClientSpace(request):
    return render(request, 'App_beta/client_space.html')

# class FreelancerCreate(LoginRequiredMixin, CreateView):
#     model = Freelancer
#     fields = ['image']
#     success_url = reverse_lazy('App_beta:service-home')

class FreelancerCreateView(LoginRequiredMixin, View):
    template_name = 'App_beta/freelancer_form.html'
    success_url = reverse_lazy('App_beta:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        freelancer = form.save(commit=False)
        freelancer.user = self.request.user
        freelancer.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        return redirect(self.success_url)

class ServiceDetailView(DetailView):
    model = Service
    template_name = "App_beta/service_detail.html"
    def get(self, request, pk) :
        x = Service.objects.get(id=pk)
        context = { 'Service' : x }
        return render(request, self.template_name, context)

class ProjectCreateView(LoginRequiredMixin, View):
    template_name = 'App_beta/apply_service.html'

    def post(self, request, pk):
        form = ApplyServiceForm(request.POST, request.FILES)
        if form.is_valid():
            project_instance = Project()
            project_instance.description = form.cleaned_data['description']
            # project_instance.attachments = form.cleaned_data['attachments'] To be added in models.py
            project_instance.pricing = form.cleaned_data['pricing']
            project_instance.expected_end_date = form.cleaned_data['delivery_date']
            project_instance.start_date = datetime.now().date()
            project_instance.user = request.user
            project_instance.service = Service.objects.get(id=pk)
            project_instance.save()

            # This line should be written here (after project_instance.save())
            project_instance.tool.set(form.cleaned_data['tools'])

            return redirect('App_beta:all')
        else:
            return render(request, self.template_name, {'form': form, 'project_pk': pk})

    def get(self, request, pk):
        form = ApplyServiceForm()
        return render(request, self.template_name, {'form': form, 'project_pk': pk})