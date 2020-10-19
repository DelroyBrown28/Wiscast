from django.urls import path
from .views import PodcastListView, PodcastInfoView, AudioDetailView


app_name = 'podcasts'

urlpatterns = [
    path('', PodcastListView.as_view(), name='list'),
    path('<slug>', PodcastInfoView.as_view(), name='info'),
    path('<podcasts_slug>/<audio_slug>', AudioDetailView.as_view(), name='audio-detail'),
]

