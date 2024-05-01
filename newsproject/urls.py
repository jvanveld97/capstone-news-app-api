from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from newsapi.views import (
    UserViewSet,
    ArticleViewSet,
    CommentViewSet,
    MoodsViewSet,
    UserSavedArticleViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"articles", ArticleViewSet, "article")
router.register(r"saved_articles", UserSavedArticleViewSet, "saved_article")
router.register(r"comments", CommentViewSet, "comment")
router.register(r"moods", MoodsViewSet, "mood")


urlpatterns = urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]
