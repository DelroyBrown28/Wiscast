from django.contrib import admin
from .models import Podcasts, PodcastAudio

admin.site.register(Podcasts)
admin.site.register(PodcastAudio)