from django.db import models
from django.contrib.auth.models import User
from .article import Article


class UserSavedArticle(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saved_articles"
    )
    article = models.JSONField()

    class Meta:
        app_label = "newsapi"
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.user.username} - {self.article['title']}"
