from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Posts
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение для изменения и удаления только для автора поста
        return obj.user == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'delete', 'retrieve']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsAuthorOrReadOnly()]
    
