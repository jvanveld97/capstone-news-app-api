from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from newsapi.models import UserSavedArticle, Article
from .articles import ArticleSerializer, ArticleViewSet
from rest_framework.generics import get_object_or_404
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class UserSavedArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSavedArticle
        fields = ("id", "user", "article")
        read_only_fields = ("user",)


class UserSavedArticleViewSet(viewsets.ModelViewSet):
    queryset = UserSavedArticle.objects.all()
    serializer_class = UserSavedArticleSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        saved_articles = self.queryset.filter(user=request.user)
        serializer = UserSavedArticleSerializer(
            saved_articles, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "You cannot delete someone else's saved article"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            article_data = serializer.validated_data.pop("article")
            article_queryset = Article.objects.filter(**article_data)

            if article_queryset.exists():
                article = article_queryset.first()
            else:
                article = Article.objects.create(**article_data)

            article_dict = {
                "url": article.url,
                "source_id": article.source_id,
                "source_name": article.source_name,
                "author": article.author,
                "title": article.title,
                "description": article.description,
                "published_at": str(article.published_at),
                "content": article.content,
                "url_to_image": article.url_to_image,
            }

            try:
                saved_article, created = UserSavedArticle.objects.get_or_create(
                    user=request.user, article=article_dict
                )
                if not created:
                    return Response(
                        {"error": "Article has already been saved."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except IntegrityError:
                return Response(
                    {"error": "An error occurred while saving the article."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(saved_article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
