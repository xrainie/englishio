from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import UserRegisterForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('account:login')


class DashboardView(TemplateView):
    template_name = 'base.html'