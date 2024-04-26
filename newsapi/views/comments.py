from rest_framework import serializers
from newsapi.models import Comment
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save(user=request.user)
        except IntegrityError:
            return Response(
                {"error": "Failed to create comment. Duplicate entry."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
