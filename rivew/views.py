from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from post.models import Posts
from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializers
from rest_framework import status
from rest_framework import permissions



class IsCommentAuthorOrPostAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if obj.post.user == request.user:
            return True

        return False


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsCommentAuthorOrPostAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

    

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"user": ["Пользователь не аутентифицирован"]}, status=status.HTTP_401_UNAUTHORIZED)

        # user = request.user

        serializer = CommentSerializers(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        post = Posts.objects.get(pk=pk) 
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.like = not like.like 
            like.save()
            message = 'unliked' if not like.like else 'liked'
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user, like=True)
            message = 'liked'
        return Response({"message": message}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)