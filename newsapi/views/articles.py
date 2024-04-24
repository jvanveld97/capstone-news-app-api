from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from newsapi.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            "url",
            "source_id",
            "source_name",
            "author",
            "title",
            "description",
            "published_at",
            "content",
            "url_to_image",
        ]


class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data)
