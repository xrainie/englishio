from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import Learner
from .forms import UserRegisterForm

# class RegisterView(CreateView):
#     template_name = 'registration/register.html'
#     form_class = UserRegisterForm
#     success_url = reverse_lazy('account:login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Learner.objects.create(user=user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class DashboardView(TemplateView):
    template_name = 'base.html'