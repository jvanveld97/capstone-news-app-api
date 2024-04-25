from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from newsapi.models import Article


# class ArticleURLField(ForeignKey):
#     def __init__(self, *args, **kwargs):
#         kwargs["to"] = Article
#         kwargs["to_field"] = "url"
#         super().__init__(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_url = models.URLField()
    # article_url = models.ForeignKey(Article, on_delete=models.CASCADE)
    # article_url = ArticleURLField(on_delete=models.CASCADE, unique=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article_url}"
