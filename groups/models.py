from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Group(models.Model):
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_groups")
    avatar = models.ImageField(upload_to="group_avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return self.title

    
class GroupMember(models.Model):
    ROLE_CHOICES = [("owner", "Owner"), ("admin", "Admin"), ("member", "Member")]
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["group", "user"], name="unique_group_member")]
    def __str__(self): 
        return f"{self.user_id} in {self.group_id} ({self.role})"
