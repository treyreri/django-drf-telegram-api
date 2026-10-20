from django.urls import path
from .views import ChannelPostListCreateView, PostDetailView
urlpatterns = [path("channels/<int:channel_id>/posts/", ChannelPostListCreateView.as_view()), path("posts/<int:pk>/", PostDetailView.as_view())]
