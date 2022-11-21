from django.contrib import admin
from .models import Article, ArticleImage, Tag, ArticleImage

admin.site.register([Tag])


class TabularInlineImages(admin.TabularInline):
    model = ArticleImage
    extra = 1
    fields = ['image']


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [TabularInlineImages]

admin.site.register(Article, ArticleAdmin)


