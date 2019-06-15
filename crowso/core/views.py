from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import forms


def project_creation_view(request):
    if request.POST:
        form = forms.ProjectCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('core:home'))
        else:
            return render(request, 'core/create_project.html', {'form': form})
    else:
        form = forms.ProjectCreationForm()
        return render(request, 'core/create_project.html', {'form': form})
