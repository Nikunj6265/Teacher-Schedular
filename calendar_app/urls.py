from django.urls import path
from calendar_app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('register/', views.Registration.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='calendar_app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<str:format>/', views.download_schedule, name='download_schedule'),
]