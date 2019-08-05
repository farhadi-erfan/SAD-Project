from django.db import models

from accounts.models import Contributor, Requester
from core.utils import validate_percent


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    value = models.PositiveIntegerField()
    deadline = models.DateField()
    picture = models.ImageField()
    attachment = models.FileField()
    subprojects_num = models.IntegerField(default=1)

    TRANSLATE = 1
    TYPE = 2
    OTHER = 3

    TYPE_CHOICES = (
        (TRANSLATE, 'translate'),
        (TYPE, 'type'),
        (OTHER, 'other')
    )

    type = models.IntegerField(choices=TYPE_CHOICES)


class RequesterProject(models.Model):
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class SubProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    percent = models.IntegerField(validators=[validate_percent])
    done = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    accepted = models.BooleanField(null=True)
    price = models.PositiveIntegerField(default=0)


class ContributorSubProject(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    sub_project = models.ForeignKey(SubProject, related_name='contributor',
                                       on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateField(null=True)
    attachment = models.FileField(null=True)

    class Meta:
        unique_together = (("contributor", "sub_project"),)

    def save(self, *args, **kwargs):
        super(ContributorSubProject, self).save()
        if not self.deadline_date:
            self.deadline_date = self.sub_project.project.deadline

