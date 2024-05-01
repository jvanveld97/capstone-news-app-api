from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from newsapi.models import UserSavedArticle
from .articles import ArticleSerializer
from rest_framework.generics import get_object_or_404


class UserSavedArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = UserSavedArticle
        fields = ("id", "user", "article")


class UserSavedArticleViewSet(viewsets.ModelViewSet):
    queryset = UserSavedArticle.objects.all()
    serializer_class = UserSavedArticleSerializer

    def list(self, request):
        saved_articles = UserSavedArticle.objects.all()
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
