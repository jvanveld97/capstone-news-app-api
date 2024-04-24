from django.db import models


class Article(models.Model):
    url = models.URLField()
    source_id = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    content = models.TextField()
    url_to_image = models.URLField()

    def __str__(self):
        return self.title
