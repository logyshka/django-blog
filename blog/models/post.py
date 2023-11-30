from django.db import models


class Post(models.Model):
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    objects = models.Manager()

    slug = models.SlugField(max_length=355, unique=True, verbose_name='URL')
    title = models.CharField(max_length=355, verbose_name='Заголовок', unique=True)
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    published_at = models.DateTimeField(null=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(verbose_name='Опубликован')

