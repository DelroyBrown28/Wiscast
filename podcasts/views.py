from django.shortcuts import render


from django.views.generic import ListView, DetailView
from .models import Podcasts


class PodcastListView(ListView):
    model = Podcasts


class PodcastInfoView(DetailView):
    model = Podcasts