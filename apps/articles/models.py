from distutils.command.upload import upload
from numbers import Real
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from slugify import slugify
from .utils import get_time


User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    parent_category = models.ForeignKey(
        verbose_name='Родительская категория',
        to='self', 
        on_delete=models.SET_NULL,
        related_name='subcategories',
        blank=True,
        null=True
         )
    
    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft')
    )

    user = models.ForeignKey(
        verbose_name='Автор статьи',
        to=User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, primary_key=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='article_images')
    status = models.CharField(
        max_length=12, 
        choices=STATUS_CHOICES, 
        default='draft')
    tag = models.ManyToManyField(
        to='Tag',
        related_name='articles',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.CASCADE, 
        related_name='articles')

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('created_at', )

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk":self.pk})


class ArticleImage(models.Model):
    image = models.ImageField(upload_to='article_images/carousel')
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='article_images'
    )

class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.article.title}'


