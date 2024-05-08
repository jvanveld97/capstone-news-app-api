from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from newsapi.views import (
    UserViewSet,
    ArticleViewSet,
    CommentViewSet,
    MoodsViewSet,
    UserSavedArticleViewSet,
    TopicViewSet,
    TopicArticlesView,
    SummarizerView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"articles", ArticleViewSet, "article")
router.register(r"saved_articles", UserSavedArticleViewSet, "saved_article")
router.register(r"comments", CommentViewSet, "comment")
router.register(r"moods", MoodsViewSet, "mood")
router.register("topics", TopicViewSet, basename="topic")
router.register(r"summarizer", SummarizerView, "summary")


urlpatterns = [
    path("topics/articles", TopicArticlesView.as_view(), name="topic-articles"),
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
    path(
        "articles/search",
        ArticleViewSet.as_view({"get": "search"}),
        name="article-search",
    ),
]
