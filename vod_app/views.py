from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q
#
from .forms import (
    DefaultSearchForm,
    UploadVideoForm,
    EmbedVideoForm,
    PictureFormset,
    CategorySearchForm,
    SpeakerSearchForm,
    DateSearchForm
)

from .helpers import (
        user_can_upload,
        generate_thumbnail,
        save_thumbnail,
        get_thumbnail_url
)

from .models import (
        Video,
        Picture,
        get_thumbnail_path
)


class Home(View):
    template = 'home.html'
    page_name = 'Home'

    def get(self, request):
        context = {
            'page_name': self.page_name
        }

        if user_can_upload(request):
            context['user_can_upload'] = True

        most_recent_video = Video.objects.latest('datetime')
        context['most_recent_video'] = most_recent_video

        return render(request,
                      self.template,
                      context)


class Search(View):
    template = 'search.html'
    page_name = 'Search'

    def get(self, request):
        context = {
            'page_name': self.page_name,
        }

        # Sort by date newest to oldest, and then by title alphabetically.
        videos = Video.objects.order_by('-datetime', 'title')

        # Get query and filter results if query is non-empty
        query = request.GET.get('query')
        if query:
            videos = Video.objects.filter(Q(title__icontains=query)
                                          | Q(description__icontains=query)
                                          | Q(speaker__icontains=query)
                                          | Q(category__icontains=query)).distinct()
            if len(videos) == 0:
                context['no_results_message'] = "No matching videos found."
                return render(request,
                              self.template,
                              context)

        # 10 videos per page
        paginator = Paginator(videos, 10, orphans=2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        if user_can_upload(request):
            context['user_can_upload'] = True

        return render(request,
                      self.template,
                      context)


class Login(LoginView):
    template_name = 'login.html'
    page_name = 'Login'
    next = reverse_lazy('vod-home')
    extra_context = {
        'page_name': page_name,
        'next': next,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if user_can_upload(self.request):
            context['user_can_upload'] = True
        return context


class Logout(LogoutView):
    next_page = reverse_lazy('vod-home')


class Upload(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template = 'upload.html'
    page_name = 'Upload'

    def get(self, request):
        context = {
            'page_name': self.page_name,
        }
        if user_can_upload(request):
            context['user_can_upload'] = True
            return render(request,
                          self.template,
                          context)
        else:
            context['denied_message'] = "You do not have permission to upload videos."
            return render(request,
                          self.template,
                          context)


class UploadFile(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template = 'upload-file.html'
    page_name = 'Upload'

    def get(self, request):
        context = {
            'page_name': self.page_name
        }
        if user_can_upload(request):
            context['user_can_upload'] = True

            video_upload_form = UploadVideoForm()
            context['video_upload_form'] = video_upload_form

            picture_formset = PictureFormset(queryset=Picture.objects.none())
            context['picture_formset'] = picture_formset

            return render(request,
                          self.template,
                          context)
        else:
            context['denied_message'] = "You do not have permission to upload videos."
            return render(request,
                          self.template,
                          context)

    def post(self, request):
        context = {
            'page_name': self.page_name
        }
        if user_can_upload(request):
            context['user_can_upload'] = True

            video_upload_form = UploadVideoForm(request.POST or None,
                                                request.FILES or None)
            context['video_upload_form'] = video_upload_form

            picture_formset = PictureFormset(request.POST or None,
                                             request.FILES or None)
            context['picture_formset'] = picture_formset

            if video_upload_form.is_valid() and picture_formset.is_valid():
                """
                Videos can be saved without any pictures.
                
                Video needs to be written to upload location in order
                to generate a thumbnail from it, hence no 'commit=False' in save(). 
                """
                video = video_upload_form.save()
                thumbnail_time = video_upload_form.cleaned_data.get('thumbnail_time')
                # Generate thumbnail
                if thumbnail_time:
                    thumbnail = generate_thumbnail(video_path=video.video_file.path,
                                                   timestamp=thumbnail_time)
                else:
                    thumbnail = generate_thumbnail(video_path=video.video_file.path)
                # Save thumbnail to filesystem
                thumbnail_path = save_thumbnail(thumbnail=thumbnail,
                                                video_path=video.video_file.name)
                # https://stackoverflow.com/a/12917845
                video.thumbnail = thumbnail_path
                video.save(update_fields=['thumbnail'])

                """If there are uploaded pictures, save these as well."""
                for picture_form in picture_formset:
                    if picture_form.is_valid() and picture_form.cleaned_data != {}:
                        picture = picture_form.save(commit=False)
                        picture.video = video
                        picture.save()
                    elif not picture_form.is_valid():
                        """Render page again to display the errors."""
                        return render(request,
                                      self.template,
                                      context)
                context['success'] = True
                context['added_video'] = video
                return render(request,
                              self.template,
                              context)
            else:
                """Render page again to display the errors."""
                return render(request,
                              self.template,
                              context)
        else:
            context['denied_message'] = "You do not have permission to upload videos."
            return render(request,
                          self.template,
                          context)


class UploadEmbed(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template = 'upload-embed.html'
    page_name = 'Upload'

    def get(self, request):
        context = {
            'page_name': self.page_name
        }
        if user_can_upload(request):
            context['user_can_upload'] = True

            video_embed_form = EmbedVideoForm()
            context['video_embed_form'] = video_embed_form

            picture_formset = PictureFormset(queryset=Picture.objects.none())
            context['picture_formset'] = picture_formset

            return render(request,
                          self.template,
                          context)
        else:
            context['denied_message'] = "You do not have permission to upload videos."
            return render(request,
                          self.template,
                          context)

    def post(self, request):
        context = {
            'page_name': self.page_name
        }
        if user_can_upload(request):
            context['user_can_upload'] = True

            video_embed_form = EmbedVideoForm(request.POST or None,
                                              request.FILES or None)
            context['video_embed_form'] = video_embed_form

            picture_formset = PictureFormset(request.POST or None,
                                             request.FILES or None)
            context['picture_formset'] = picture_formset

            if video_embed_form.is_valid() and picture_formset.is_valid():
                """Videos can be saved without any pictures."""
                video = video_embed_form.save(commit=False)
                video.thumbnail_url = get_thumbnail_url(video.embed_link)
                video.save()

                """If there are uploaded pictures, save these as well."""
                for picture_form in picture_formset:
                    if picture_form.is_valid() and picture_form.cleaned_data != {}:
                        picture = picture_form.save(commit=False)
                        picture.video = video
                        picture.save()
                    elif not picture_form.is_valid():
                        """Render page again to display the errors."""
                        return render(request,
                                      self.template,
                                      context)
                context['success'] = True
                context['added_video'] = video
                return render(request,
                              self.template,
                              context)
            else:
                """Render page again to display the errors."""
                return render(request,
                              self.template,
                              context)
        else:
            context['denied_message'] = "You do not have permission to upload videos."
            return render(request,
                          self.template,
                          context)


class VideoDetail(DetailView):
    model = Video
    template_name = 'video-detail.html'

    """Add all Pictures related to this Video to the context."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if user_can_upload(self.request):
            context['user_can_upload'] = True

        related_pictures = Picture.objects.filter(video__pk=self.object.pk)
        print(related_pictures)
        print("\n")
        for picture in related_pictures:
            print(picture)
        """only add to context if there is something to add!"""
        context['related_pictures'] = related_pictures
        return context
