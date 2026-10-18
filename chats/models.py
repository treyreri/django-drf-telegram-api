from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.db.models import Q, F

class Chat(models.Model):
    user_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.СASCADE, related_name="chats_as_user_1")
    user_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "chats_as_user_1")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.CheckConstraint(
                    condition=~Q(user_1=F("user_2")), 
                    name="chat_users_different"), 
                    models.UniqueConstraint(fields=["user_1", "user_2"], 
                    name="unique_chat_pair")]


#Q позволяет описывать условия для полей модели
# F позволяет обратиться к значению другого поля непосредственно в базе данных
#Символ ~ означает логическое отрицание, то есть NOT
#в общем означает, что user_1 и user_2 должны быть разными