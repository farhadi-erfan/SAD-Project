from datetime import datetime
from django import forms

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView

from accounts.models import Requester, User, Contributor
from core.models import Project, RequesterProject, SubProject, ContributorSubProject
from .forms import UserSignupForm


class SignupView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


@login_required
def view_profile(request):
    if request.user.is_requester:
        projects = Project.objects.filter(
            requesterproject__requester=Requester.objects.get(user=request.user)
        )
        return render(request, 'profile.html', {
            'user': request.user,
            'projects': projects,
        })
    else:
        csp = ContributorSubProject.objects.select_related('sub_project').filter(
            contributor=Contributor.objects.get(user=request.user)
        ).values_list('sub_project_id', flat=True)
        subprojects = SubProject.objects.filter(
            id__in=csp
        ).order_by('contributor__deadline_date')
        return render(request, 'profile.html', {
            'user': request.user,
            'projects': subprojects
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


class UpdateProfile(UpdateView):
    model = User
    fields = ['name', 'address', 'phone_number', 'picture']
    template_name = 'edit_profile.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('core:home')
