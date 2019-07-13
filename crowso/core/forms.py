from django import forms
from django.forms import widgets

from core.models import Project, ContributorSubProject


class ProjectCreationForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'attachment', 'picture', 'subprojects_num',
                  'value', 'type', 'deadline']

class ContributorSubProjectForm(forms.ModelForm):

    class Meta:
        model = ContributorSubProject
        fields = ['attachment']


class ChargeCreditForm(forms.Form):
    charge_amount = forms.IntegerField(min_value=5000, max_value=5000000, initial=5000)


class WithdrawForm(forms.Form):
    card_number = forms.CharField(min_length=16, max_length=16)
