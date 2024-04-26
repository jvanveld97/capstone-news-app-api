from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from newsapi.models import Article


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_url = models.URLField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article_url}"
