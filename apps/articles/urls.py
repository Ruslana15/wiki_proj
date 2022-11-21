from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, CommentCreateDeleteView, TagViewSet


router = DefaultRouter()
router.register('article', ArticleViewSet, 'article')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('tags', TagViewSet, 'tags')
urlpatterns = [
]
urlpatterns += router.urls
