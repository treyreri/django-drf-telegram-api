from django.urls import path
from .views import ChannelListCreateView, ChannelDetailView, FollowChannelView, FollowingListView, IsFollowingView
urlpatterns = [
 path("", ChannelListCreateView.as_view()), path("following/", FollowingListView.as_view()),
 path("<int:channel_id>/follow/", FollowChannelView.as_view()), path("<int:channel_id>/is-following/", IsFollowingView.as_view()),
 path("<int:pk>/", ChannelDetailView.as_view()),
]
