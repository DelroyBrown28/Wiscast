from django.urls import path
from .views import PodcastListView, PodcastInfoView


app_name = 'podcasts'

urlpatterns = [
    path('', PodcastListView.as_view(), name='list'),
    path('<slug>', PodcastInfoView.as_view(), name='info'),
]

