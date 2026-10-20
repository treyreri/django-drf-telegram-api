
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.urls")),
    path("api/profiles/", include("profiles.urls")),
    path("api/chats/", include("chats.urls")),
    path("api/messages/", include("messages.urls")),
    path("api/groups/", include("groups.urls")),
    path("api/group-messages/", include("group_messages.urls")),
    path("api/channels/", include("channels.urls")),
    path("api/posts/", include("posts.urls")),
]
