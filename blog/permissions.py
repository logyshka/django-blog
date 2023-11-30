from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from blog.models import Post


class CanUpdatedThePost(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        slug = getattr(request.data, 'slug', None)
        if not slug:
            return False
        return Post.objects.filter(slug=slug, author=request.user).exists()
