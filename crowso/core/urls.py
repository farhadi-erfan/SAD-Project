from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_project', views.project_creation_view, name='create_project'),
]
