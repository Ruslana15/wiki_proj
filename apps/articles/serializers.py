from rest_framework import serializers
from django.db.models import Avg

from apps.articles.permissions import IsStaff

from .models import (
    Article,
    Tag,
    Comment,
    ArticleImage,
    Category
)


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('user', 'title', 'image', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        representation['carousel'] = ArticleImageSerializer(
            instance.article_images.all(), many=True).data
        return representation

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = 'image', 

class ArticleCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    carousel_img = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    permission_classes = [IsStaff]

    class Meta:
        model = Article
        fields = '__all__'
        # exclude = ('tag', )

    def create(self, validated_data):
        carousel_images = validated_data.pop('carousel_img')
        tag = validated_data.pop('tag')
        article = Article.objects.create(**validated_data)
        article.tag.set(tag)
        images = []
        for image in carousel_images:
            images.append(ArticleImage(article=article, image=image))
        ArticleImage.objects.bulk_create(images)
        return article
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Comment
        exclude = ['article']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, attrs):
        tag = attrs.get('title')
        if Tag.objects.filter(title=tag).exists():
            raise serializers.ValidationError('Tag with this name already exists')
        return attrs

class CurrentArticleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['article']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ArticleFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title')

class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('user', 'title', 'image', 'slug', 'views_count')
        # Article.objects.filter(max('views_count'))

    # def to_representation(self, instance):
    #     instance = super().to_representation(instance)
    #     print(instance)
    #     return instance


class ArticleSerializerTop(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('user_id', 'title', 'image', 'slug', 'views_count')
