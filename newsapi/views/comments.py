from rest_framework import serializers
from newsapi.models import Comment
from rest_framework import viewsets
from rest_framework.response import Response


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Custom action to filter comments by article URL
    def list(self, request):
        article_url = request.query_params.get("article_url")
        if article_url:
            queryset = Comment.objects.filter(article_url=article_url)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(request)
