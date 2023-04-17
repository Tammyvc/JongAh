from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('confirm/',views.ConfirmView.as_view(),name='confirm'),
    path('password_reset/',views.PasswordForgetView.as_view(),name='password_reset'),
    path('logout/',views.LoggoutView.as_view(),name='logout'),
    path('<str:username>/user_center/',views.user_center,name='user_center'),
    path('<str:user_name>/user_edit/',views.edit_profile,name='user_edit'),
    path('<str:user_name>/cover/',views.cover,name='user_cover'),
    path('<str:user_name>/avatar/',views.avatar,name='user_avatar'),
]
