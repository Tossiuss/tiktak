from django.urls import path
from .views import LikeViewSet,CommentView


urlpatterns = [
    path('posts/<int:pk>/like/', LikeViewSet.as_view({'post': 'toggle_like'})),
    path('comment/', CommentView.as_view({'post': 'create', 'get': 'list'})),
    path('comment/<int:pk>/', CommentView.as_view({'delete': 'destroy'})),
]
