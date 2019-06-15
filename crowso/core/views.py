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


def home(request):

    def get_user_projects(user):
        import datetime
        lipsum = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
        return [{'name': 'ali', 'value': 10, 'description': lipsum, 'deadline': datetime.date.today}, {'name': 'bali', 'value': 30, 'description': lipsum, 'deadline': datetime.date.today}, {'name': 'vali', 'value': 40, 'description': lipsum, 'deadline': datetime.date.today}]
    user = request.user
    projects = get_user_projects(user)
    return render(request, 'core/home.html', {'projects': projects})
