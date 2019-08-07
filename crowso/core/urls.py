from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create_project', views.project_creation_view, name='create_project'),
    path('credit', views.credit, name='credit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path(r'work/<int:subproject_id>', views.work, name='work'),
    path(r'accept_task/<int:project_id>/', views.accept_task, name='accept_task'),
    path(r'accept_subproject/<int:sp_id>', views.accept_subproject, name='accept_subproject'),
    path(r'deny_subproject/<int:sp_id>', views.deny_subproject, name='deny_subproject'),
    path(r'project_view/<int:project_id>', views.project_state_view, name='project_view'),
    path(r'get_result/<int:project_id>', views.download_all_exports, name='get_result')
]
