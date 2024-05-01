from django.db import models


# class Article(models.Model):
#     url = models.URLField()
#     source_id = models.CharField(max_length=255)
#     source_name = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     published_at = models.DateTimeField()
#     content = models.TextField()
#     url_to_image = models.URLField()


#     def __str__(self):
#         return self.title
class Article(models.Model):
    url = models.URLField()
    source_id = models.CharField(max_length=255, null=True, blank=True, default="N/A")
    source_name = models.CharField(max_length=255, null=True, blank=True, default="N/A")
    author = models.CharField(max_length=255, null=True, blank=True, default="N/A")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default="N/A")
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True, default="N/A")
    url_to_image = models.URLField(null=True, blank=True, default="N/A")

    class Meta:
        app_label = "newsapi"

    def save(self, *args, **kwargs):
        if not self.source_id:
            self.source_id = "N/A"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
