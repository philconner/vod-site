from django.db import models
from datetime import date


def get_thumbnail_path(instance=None, filename=None):
    today = date.today()
    base_dir = 'thumbnails'
    return today.strftime(f"{base_dir}/%Y/%m/%d/")

class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500,
                                   blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    speaker = models.CharField(max_length=50)

    # for uploaded videos
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/',
                                  blank=True,
                                  null=True)
    thumbnail = models.FileField(upload_to=get_thumbnail_path,
                                 blank=True)

    # for embedded youtube videos
    embed_link = models.URLField(blank=True,
                                 null=True)
    thumbnail_url = models.URLField(blank=True)

    GENERAL = 'general'
    COLLOQ = 'colloq'
    CLASS = 'class'
    DEFENSE = 'defense'
    CATEGORIES = [
        (GENERAL, 'General'),
        (COLLOQ, 'Colloquium'),
        (CLASS, 'Class'),
        (DEFENSE, 'PhD Defense'),
    ]
    category = models.CharField(max_length=20,
                                choices=CATEGORIES)


class Picture(models.Model):
    """
    There can be zero or more Pictures attached to ONE Video.

    If the Video of any given Picture is deleted, delete all other
    Pictures that were attached to that Video as well.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    picture_file = models.FileField(upload_to='images/%Y/%m/%d/')
    caption = models.CharField(max_length=100)


class Tag(models.Model):
    text = models.CharField(max_length=30)
    videos = models.ManyToManyField(Video)
