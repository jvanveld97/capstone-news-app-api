from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from .mood import Mood
from newsapi.models import article


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_url = models.URLField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    mood = models.ForeignKey(
        Mood, on_delete=models.CASCADE, related_name="comments", null=True
    )
