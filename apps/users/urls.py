from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verification/<email>/', views.email_verification, name='email-verification'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('list/', views.UserListView.as_view(), name='users_list'),
]
