from django.contrib.auth import forms

from .models import User, Requester, Contributor


class UserSignupForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        self.requester = kwargs.pop('requester', False)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.requester:
            user.is_requester = True
        else:
            user.is_contributor = True
        user.save()

        if self.requester:
            Requester.objects.create(user=user)
        else:
            Contributor.objects.create(user=user)
        return user