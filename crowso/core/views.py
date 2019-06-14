from django.shortcuts import render
from . import forms


def project_creation_view(request):
    form = forms.ProjectCreationForm()

    return render(request, 'core/create_project.html', {'form': form})
