from django.urls import path
from .views import GroupMessageListCreateView, GroupMessageDeleteView
urlpatterns = [path("groups/<int:group_id>/messages/", GroupMessageListCreateView.as_view()), path("group-messages/<int:pk>/", GroupMessageDeleteView.as_view())]
