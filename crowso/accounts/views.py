import ajax as ajax
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import Requester
from core.models import Project, RequesterProject, SubProject
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


@login_required
def view_subprojects(request):
    template = ''
    projects = Project.objects.annotate().filter(deadline__gt=datetime.today())
    for p in projects:
        p.not_assigned_subprojects = SubProject.objects.filter(
            assigned=False,
            project=p
        ).count()
    return render(request, template_name=template, context={
        'projects': projects
    })


def accept_subproject():
    pass