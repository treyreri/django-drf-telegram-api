from django.db import models


from django.db import models
class Post(models.Model):
    channel = models.ForeignKey(
    "channels.Channel",
    on_delete=models.CASCADE,
    related_name="posts" )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    content = models.TextField(max_length=20000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title