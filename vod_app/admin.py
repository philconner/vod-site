from django.contrib import admin
from .models import Video, Picture, Tag

admin.site.register([Video, Picture, Tag])