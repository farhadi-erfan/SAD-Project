from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_project', views.project_creation_view, name='create_project'),
    path('credit', views.credit, name='credit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path(r'work/<int:subproject_id>', views.work, name='work'),
    path(r'accept_task/<int:project_id>/', views.accept_task, name='accept_task')
]
