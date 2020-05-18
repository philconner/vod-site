import os
import cv2
import urllib.parse as urlparse
#
from .models import get_thumbnail_path
from django.conf import settings

def user_can_upload(request):
    """Return whether or not a user should be able to upload a video."""
    return request.user.groups.filter(name='Faculty').exists()

def convert_to_ms(timestamp):
    """Convert a H:MM:SS timestamp to milliseconds."""
    h, m, s = timestamp.split(':')

    try:
        return ((int(h) * 3600) + (int(m) * 60) + int(s)) * 1000
    except ValueError:
        return "Invalid input, enter integers for each field."

def generate_thumbnail(video_path, timestamp="0:00:00"):
    """Take in an absolute path to a video and a timestamp, and return a thumbnail."""
    video = cv2.VideoCapture(video_path)
    timestamp_ms = convert_to_ms(timestamp)
    video.set(0, timestamp_ms)
    success, image = video.read()
    if success:
        # Thumbnail can be captured
        return image
    else:
        # Given timestamp is outside the duration of the video
        return "Provided timestamp is not within the confines of the video."

def save_thumbnail(thumbnail, video_path):
    video_filename = os.path.basename(video_path)
    filename = video_filename + '.thumb.jpg'
    destination_dir = settings.MEDIA_ROOT + get_thumbnail_path()
    destination_file = destination_dir + filename

    # Destination needs to exist before calling imwrite()
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, mode=0o755)
    cv2.imwrite(destination_file, thumbnail)

    # Return filename path relative to MEDIA_ROOT: https://stackoverflow.com/a/12917845
    return get_thumbnail_path() + filename

def get_thumbnail_url(embed_link):
    """Take in an embed link and return a thumbnail url.
    Expected format of embed_link: https://www.youtube.com/embed/ID1KR37bqnQ"""
    url = urlparse.urlparse(embed_link)
    video_id = os.path.basename(url.path)
    thumbnail_url = "https://img.youtube.com/vi/{}/0.jpg".format(video_id)
    return thumbnail_url
