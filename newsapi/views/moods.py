from rest_framework import serializers
from newsapi.models import Mood
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import permissions


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ["id", "name"]


class MoodsViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer

    def list(self, request):
        moods = Mood.objects.all()
        serializer = MoodSerializer(moods, many=True, context={"request": request})
        return Response(serializer.data)
