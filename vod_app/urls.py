from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
#
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='vod-home'),
    path('search/', views.Search.as_view(), name='vod-search'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('upload/', views.Upload.as_view(), name='vod-upload'),
    path('upload-file/', views.UploadFile.as_view(), name='vod-upload-file'),
    path('upload-embed/', views.UploadEmbed.as_view(), name='vod-upload-embed'),
    path('videos/<int:pk>/', views.VideoDetail.as_view(), name='video-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
