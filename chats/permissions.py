from rest_framework.permissions import BasePermission

class IsChatParticipant(BasePermission):
    """Object-level permission: only either participant can access a chat."""
    message = "You are not a participant in this chat."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.pk in (obj.user_1_id, obj.user_2_id)
