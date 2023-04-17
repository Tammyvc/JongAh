from django import forms

class UserProfileForm(forms.Form):
    """UserProfile的表单"""
    nickname = forms.CharField(max_length=128)
    sex = forms.CharField(max_length=10)
    introduction = forms.CharField(max_length=255)
