from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    phone_number = models.CharField(max_length=12)
    is_contributor = models.BooleanField(default=False)
    is_requester = models.BooleanField(default=False)
    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )

    JUNIOR = 0
    SENIOR = 1
    LEVEL_CHOICES = (
        (JUNIOR, 'junior'),
        (SENIOR, 'senior')
    )
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES, default=JUNIOR)


class Requester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
