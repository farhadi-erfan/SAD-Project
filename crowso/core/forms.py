from django import forms
from django.forms import widgets

from core.models import Project


class ProjectCreationForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'attachment', 'picture',
                  'value', 'type', 'deadline']
