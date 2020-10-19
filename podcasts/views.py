from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from memberships.models import UserMembership
from .models import Podcasts


class PodcastListView(ListView):
    model = Podcasts


class PodcastInfoView(DetailView):
    model = Podcasts


class AudioDetailView(View):
    def get(self, request, podcasts_slug, audio_slug, *args, **kwargs):
        podcast_qryset = Podcasts.objects.filter(slug=podcasts_slug)
        if podcast_qryset.exists():
            podcast = podcast_qryset.first()

        # Audio query set
        audio_qryset = podcast.audio.filter(slug=audio_slug)
        if podcast_qryset.exists():
            podcast = podcast_qryset.first()

        user_membership = UserMembership.objects.filter(
            user=request.user).first()
        user_membership_type = user_membership.membership.membership_type

        podcast_allowed_mem_types = podcast.allowed_memberships.all()

        context = {
            'object': None
        }

        if podcast_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'object': podcast}

        return render(request, 'podcasts/audio_detail.html')
