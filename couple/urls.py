from django.urls import path
from . import views

app_name = 'couple'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('image-text/<str:category_name>/<str:post_slug>/',views.PostDetailView.as_view(),name='post_detail'),
    path('search/',views.search,name='search'),
    path('like_post/',views.like_post,name='like_post'),
    path('comment_control/',views.comment_control,name='comment_control'),
    path('share_post/<int:post_id>/',views.share_post,name='share_post'),
    path('image-text/<str:category_name>/',views.category_detail,name='category_detail'),
    path('video/we_get_married/',views.wgm_video,name='wgm_video'),
    path('video/we_get_married/<str:video_slug>/',views.wgm_video_detail,name='wgm_video_detail'),
    path('latest/',views.latest_post,name='latest'),
    path('upload_image/', views.upload_image,name='upload_image'),
]
