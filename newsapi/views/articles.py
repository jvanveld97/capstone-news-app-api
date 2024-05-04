from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from newsapi.models import Article
from django.conf import settings
import requests


def get_news_data(country, api_key, category=None, q=None):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}&pageSize=100"
    if category:
        url += f"&category={category}"
    # elif q:
    #     url += f"&q={q}"
    response = requests.get(url)
    return response.json()


def search_news_data(api_key, q=None):
    url = f"https://newsapi.org/v2/everything?language=en&q={q}&sortBy=relevancy&apiKey={api_key}&pageSize=100"
    if q:
        url += f"&q={q}"
    response = requests.get(url)
    return response.json()


class ArticleSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

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
        category = request.query_params.get("category", None)
        news_data = get_news_data(
            country="us", api_key=settings.NEWS_API_KEY, category=category
        )

        articles = []
        for article_data in news_data["articles"]:
            source = article_data.get("source", {})
            article = Article(
                url=article_data["url"],
                source_id=source.get("id"),
                source_name=source.get("name"),
                author=article_data.get("author"),
                title=article_data["title"],
                description=article_data.get("description"),
                published_at=article_data["publishedAt"],
                content=article_data.get("content"),
                url_to_image=article_data.get("urlToImage"),
            )
            article.save()
            articles.append(article)

        serializer = ArticleSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def search(self, request):
        query = request.query_params.get("q", None)
        if query:
            search_data = search_news_data(api_key=settings.NEWS_API_KEY, q=query)

            articles = []
            for article_data in search_data["articles"]:
                source = article_data.get("source", {})
                article = Article(
                    url=article_data["url"],
                    source_id=source.get("id"),
                    source_name=source.get("name"),
                    author=article_data.get("author"),
                    title=article_data["title"],
                    description=article_data.get("description"),
                    published_at=article_data["publishedAt"],
                    content=article_data.get("content"),
                    url_to_image=article_data.get("urlToImage"),
                )
                article.save()
                articles.append(article)

            serializer = ArticleSerializer(
                articles, many=True, context={"request": request}
            )
            return Response(serializer.data)
        else:
            return Response(
                {"error": "No search query provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
