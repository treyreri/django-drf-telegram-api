from django.db import models

from django.conf import settings

class GroupMessage(models.Model):
    group = models.ForeignKey("groups.Group" , on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="send_group_messages" )
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
    def __str__(self):
            return f"Group message {self.pk}"