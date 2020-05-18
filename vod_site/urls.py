# vod_site URL Configuration

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('vod_app.urls')),
    path('admin/', admin.site.urls)
]

# Add debug toolbar to debug/ if DEBUG=True
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

