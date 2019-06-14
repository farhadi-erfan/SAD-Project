from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='crowso/base.html'), name='home'),
    path('create_project', views.project_creation_view, name='create_project'),
]
