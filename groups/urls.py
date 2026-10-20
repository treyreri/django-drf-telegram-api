from django.urls import path
from .views import GroupListCreateView, GroupDetailView, GroupMemberListCreateView, GroupMemberRoleView, LeaveGroupView
urlpatterns = [
 path("", GroupListCreateView.as_view()), path("<int:pk>/", GroupDetailView.as_view()),
 path("<int:group_id>/members/", GroupMemberListCreateView.as_view()),
 path("<int:group_id>/members/<int:pk>/", GroupMemberRoleView.as_view()),
 path("<int:group_id>/members/me/", LeaveGroupView.as_view()),
]
