from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter
from rest_framework.generics import ListAPIView 

# from rest_framework.generics import (
#     ListAPIView,
#     RetrieveAPIView,
#     DestroyAPIView, 
#     UpdateAPIView, 
#     CreateAPIView)

from .models import (
    Article,
    Tag,
    Comment,
    Category
)
from .serializers import (
    ArticleListSerializer,
    ArticleSerializer,
    ArticleImageSerializer,
    ArticleCreateSerializer,
    CommentSerializer,
    TagSerializer,
    CategorySerializer,
    HomepageSerializer,
    ArticleSerializerTop
)
from .permissions import IsOwner, IsStaff
from apps.articles import serializers

# class PostListView(ListAPIView):
#     # queryset = Post.objects.filter(status='open')
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user__username']
    filterset_fields = ['tag']
    ordering_fields = ['created_at']
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'create':
            return ArticleCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['comment']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        if self.action in ['article']:
            self.permission_classes = [IsStaff]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        article = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

    def retrieve(self, request, *args, **kwargs):
        instance: Article = self.get_object() # Article
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

class CommentCreateDeleteView(
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]



class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = TagSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleFilter(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title']

class HomepageViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = HomepageSerializer
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user__username']
    filterset_fields = ['tag']
    ordering_fields = ['created_at']
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return HomepageSerializer
        elif self.action == 'create':
            return ArticleCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['comment']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        if self.action in ['article']:
            self.permission_classes = [IsStaff]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        article = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

    # def retrieve(self, request, *args, **kwargs):
    #     instance: Article = self.get_object.order_by('-views_count').values() # Homepage
    #     instance.views_count += 1
    #     instance.save()
    #     return super().retrieve(request, *args, **kwargs)
    @action(methods=["GET"], detail=False, url_path="test")
    def first_ten_top(self, request):
        articles = Article.objects.order_by('-views_count').values()
        print(articles)
        serializer = ArticleSerializerTop(articles, many=True).data[:10]

        return Response(data=serializer)


"""  
actions

create() - POST
retrieve() - GET /post/1/
list() - GET /post/
destroy() - DELETE /post/1/
partial_update() - PATCH /post/1/
update() - PUT /post/1/
"""

