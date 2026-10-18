from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class Channel(models.Model):
    TYPE_CHOICES = [ ("public" , "Public") , ("private" , "Private") ]
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=2000)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="public")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_channels")
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)[:140] or 'channel'}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    def __str__(self): return self.title

#Slug делает адрес понятнее человеку. Но само наличие поля slug ещё не создаёт URL — для этого нужно настроить маршруты Django
#НАПРИМЕР ССЫЛКА http://127.0.0.1:8000/channels/python-developers-a1b2c3d4/ . Здесь python-developers-a1b2c3d4 — это slug

class Following(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_followings")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name = "followers")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user" , "channel"] , name="unique_channel_following")]
    def __str__(self):
        return f"{self.user_id} follows {self.channel_id}"