from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('confirm/',views.ConfirmView.as_view(),name='confirm'),
    path('password_reset/',views.PasswordForgetView.as_view(),name='password_reset'),
    path('logout/',views.LoggoutView.as_view(),name='logout'),
    path('<str:username>/settings/',views.user_settings,name='settings'),
    path('<str:user_name>/edit/',views.UserEditView.as_view(),name='user_edit'),
]
