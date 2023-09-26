
from rest_framework import generics
import django_filters
from .filters import PostFilter
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Posts
from rest_framework import permissions
from like.serializers import LikeSerializer
from like.models import Like
from rest_framework.decorators import action



class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
    

    def get(self, request, *args, **kwargs):
        posts = self.queryset.filter(is_active=True)
        serializer = self.serializer_class(posts, many=True)

        return Response(serializer.data)


class PostView(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['post', 'delete', 'retrieve','get']


    def create(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return Response({"user": ["Пользователь не аутентифицирован"]}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = self.get_object()  # Получаем объект поста по переданному pk
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)



class PostCategorySearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = PostFilter


