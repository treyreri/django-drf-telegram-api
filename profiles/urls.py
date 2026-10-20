from django.urls import path
from .views import ProfileListView, ProfileDetailView, MyProfileView, AvatarListCreateView, AvatarDetailView
urlpatterns = [
    path("", ProfileListView.as_view(), name="profile-list"),
    path("me/", MyProfileView.as_view(), name="profile-me"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
]
