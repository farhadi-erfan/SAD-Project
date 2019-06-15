from django.urls import include
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', views.SignupView.as_view(), name='signup'),
    # path('supervisor', views.SupervisorSignUpView.as_view(), name='create_supervisor'),
    path('profile', views.view_profile, name='show_profile')
]