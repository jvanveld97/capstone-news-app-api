from rest_framework import serializers
from rest_framework.response import Response
from newsapi.models import Topic
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import requests
from django.conf import settings


def get_topics_data(api_key, q=None):
    url = f"https://newsapi.org/v2/everything?apiKey={api_key}&q={q}&language=en&sortBy=relevancy"
    if q:
        url += f"&q={q}"
    response = requests.get(url)
    return response.json()


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name"]


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        topics = Topic.objects.filter(user=request.user)
        articles_by_topic = {}

        for topic in topics:
            news_data = get_topics_data(api_key=settings.NEWS_API_KEY, q=topic.name)

            articles = []
            for article_data in news_data["articles"]:
                source = article_data.get("source", {})
                article = {
                    "url": article_data["url"],
                    "source_id": source.get("id"),
                    "source_name": source.get("name"),
                    "author": article_data.get("author"),
                    "title": article_data["title"],
                    "description": article_data.get("description"),
                    "published_at": article_data["publishedAt"],
                    "content": article_data.get("content"),
                    "url_to_image": article_data.get("urlToImage"),
                }
                articles.append(article)

            articles_by_topic[topic.name] = articles

        serialized_data = []
        for topic_name, articles in articles_by_topic.items():
            serialized_data.append({"topic": topic_name, "articles": articles})

        return Response(serialized_data)
