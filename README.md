# vod_site
A django web-app intended for hosting academic videos and related images.
I wrote this as a project at a previous job, to replace a very old site that served a similar purpose.

## How it works
Videos can be uploaded with zero or more pictures, and uploading is restricted to users in the
'Faculty' group. Of course, in production an ldap plugin or similar would be used to retrieve group memberships.

Uploaded videos can be in the form of a video file, or an embedded YouTube video link.
If uploading a video file, a timestamp can be provided in H:MM:SS form, and will be used
to generate a thumbnail for the video. If a timestamp is not provided, 0:00:00 will
be used instead. For embedded YouTube videos, the thumbnail URL will be grabbed using the video ID.
