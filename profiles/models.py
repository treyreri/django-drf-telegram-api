from django.db import models

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "profile")
    bio = models.TextField(blank=True, max_length=1000)
    city = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Profile : {self.phone_number}"

class Avatar(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = "avatars")
    image = models.ImageField(upload_to="avatars/" , 
                        validators=[FileExtensionValidator (["jpg" , "jpeg" , "png" , "webp"])])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Avatar {self.pk} for {self.profile_id}"
    