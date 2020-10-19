from django.db import models
from django.urls import reverse
from memberships.models import Membership


class Podcasts(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:info', kwargs={'slug': self.slug})

    @property
    def audio(self):
        return self.podcastaudio_set.all().order_by('position')


class PodcastAudio(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    podcast = models.ForeignKey(Podcasts, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    audio_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('podcasts:audio-detail', kwargs={
            'podcasts_slug': self.podcast.slug,
            'audio_slug': self.slug
        })
 