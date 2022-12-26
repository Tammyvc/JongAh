from django.contrib import admin
from .models import Profile,CustomUser,ConfirmString

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','is_active','has_confirmed','last_login','c_time')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','sex','photo')

@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    list_display = ('code','user','c_time')

