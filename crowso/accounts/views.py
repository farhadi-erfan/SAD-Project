from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import Requester
from core.models import Project, RequesterProject
from .forms import UserSignupForm


class SignupView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


@login_required
def view_profile(request):
    projects = Project.objects.filter(
        requesterproject__requester=Requester.objects.get(user=request.user)
    )
    return render(request, 'profile.html', {
        'user': request.user,
        'projects': projects
    })
