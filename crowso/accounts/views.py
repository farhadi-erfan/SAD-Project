from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserSignupForm


class SignupView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'

