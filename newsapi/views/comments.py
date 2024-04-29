from rest_framework import serializers
from newsapi.models import Comment
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import permissions


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed for the owner
        return obj.user == request.user


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the user is the owner of the comment
        if instance.user != request.user:
            return Response(
                {"error": "You are not authorized to update this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save()
        return Response(serializer.data)
