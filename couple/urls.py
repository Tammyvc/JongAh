from django.urls import path
from . import views

app_name = 'couple'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('wgm/<int:wgm_id>/',views.PostDetailView.as_view(),name='wgm'),
]
