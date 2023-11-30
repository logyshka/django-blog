from datetime import datetime
from typing import Any

from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from blog.models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'content', 'slug',
            'is_published',
        )

    slug = serializers.SerializerMethodField()
    is_published = serializers.BooleanField(default=False)
    content = serializers.CharField(required=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        title = attrs.get('title')
        now = datetime.now(settings.TIME_ZONE).timestamp()
        slug = slugify(f'{title}-{now}')

        if Post.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                {'title': 'Пост с таким названием уже существует'}
            )

        if attrs.get('is_published'):
            attrs.update(published_at=datetime.now(settings.TIME_ZONE))

        author = self.context.get('request').user
        attrs.update(slug=slug, author=author)
        return attrs


class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'content', 'slug',
            'author', 'created_at', 'updated_at',
            'published_at',
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    is_published = serializers.BooleanField(required=False)

    class Meta:
        model = Post
        fields = (
            'title', 'content', 'slug',
            'is_published',
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        title = attrs.pop('title', None)
        content = attrs.pop('content', None)
        is_published = attrs.pop('is_published', None)

        if title:
            now = datetime.now(settings.TIME_ZONE).timestamp()
            slug = slugify(f'{title}-{now}')

            if Post.objects.filter(slug=slug).exists():
                raise serializers.ValidationError(
                    {'title': 'Пост с таким названием уже существует'}
                )

            attrs.update(slug=slug, title=title)

        if content:
            attrs.update(content=content)

        if is_published:
            published_at = datetime.now(settings.TIME_ZONE)
            attrs.update(is_published=is_published, published_at=published_at)

        return attrs


class PostUpdateTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'slug',
        )

    slug = serializers.CharField(required=True)
    title = serializers.CharField(required=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        title = attrs.get('title')
        now = datetime.now(settings.TIME_ZONE).timestamp()
        slug = slugify(f'{title}-{now}')

        if Post.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                {'title': 'Пост с таким названием уже существует'}
            )

        attrs.update(slug=slug, title=title)


class PostUpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'content', 'slug',
        )

    slug = serializers.CharField(required=True)
    content = serializers.CharField(required=True)


class PostUpdatePublishedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'is_published', 'slug',
        )

    slug = serializers.CharField(required=True)
    is_published = serializers.BooleanField(required=True)

    def update(self, instance: Post, validated_data: dict[str, Any]) -> Post:
        instance.published_at = datetime.now(settings.TIME_ZONE)
        return super().update(instance, validated_data)


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'slug',
        )

    slug = serializers.CharField(required=True)
