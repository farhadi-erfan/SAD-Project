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
    path(r'accept_task/<int:subproject_id>/', views.accept_task, name='accept_task'),
    path('submit_work/<str:project>/', views.submit_work, name='submit_work')
]
