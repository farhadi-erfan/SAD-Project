from django.contrib.auth import forms
from django.forms import CheckboxInput
from .models import User, Requester, Contributor


class UserSignupForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'phone_number', 'address', 'picture', 'is_requester')

    def __init__(self, *args, **kwargs):
        self.requester = kwargs.pop('requester', False)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save()
        if user.is_requester:
            Requester.objects.create(user=user)
        else:
            Contributor.objects.create(
                user=user,
                level=Contributor.JUNIOR
            )
        return user