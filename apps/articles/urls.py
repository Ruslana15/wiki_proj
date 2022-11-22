from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, CommentCreateDeleteView, TagViewSet, CategoryViewSet


router = DefaultRouter()
router.register('article', ArticleViewSet, 'article')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('tags', TagViewSet, 'tags')
router.register('categories', CategoryViewSet, 'category')
urlpatterns = [
]
urlpatterns += router.urls
