from django import forms
#
from .models import Video, Picture


"""Search by title"""
class DefaultSearchForm(forms.Form):
    query = forms.CharField(max_length=50)


"""Search by category"""
class CategorySearchForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['category']


"""Search by speaker"""
class SpeakerSearchForm(forms.Form):
    query = forms.CharField(max_length=50)


"""Search by date"""
class DateSearchForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.SelectDateWidget())


class UploadVideoForm(forms.ModelForm):
    """thumbnail_time needs to be string of format H:MM:SS"""
    thumbnail_time = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'H:MM:SS'}))
    # , widget = forms.widgets.TextInput(attrs={'required': False})

    class Meta:
        model = Video
        exclude = [
            'datetime',
            'embed_link',
            'thumbnail',
        ]
        widgets = {
            'video_file': forms.FileInput(attrs={'required': True})
        }


class EmbedVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = [
            'datetime',
            'video_file',
            'thumbnail',
        ]
        widgets = {
            'embed_link': forms.URLInput(attrs={'required': True,
                                                'data-toggle': 'tooltip',
                                                'title': 'https://www.youtube.com/embed/VIDEO_ID_HERE'})
        }


"""Formset for the Picture model to be able to add or remove forms dynamically"""
PictureFormset = forms.modelformset_factory(Picture,
                                            exclude=['video'],
                                            extra=1,
                                            widgets={
                                                'picture_file': forms.FileInput(),
                                                'caption': forms.Textarea(),
                                            })
