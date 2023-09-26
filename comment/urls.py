from django.urls import path
from .views import CommentView

urlpatterns = [
    path('comment/', CommentView.as_view({'post': 'create', 'get': 'list'})),
    path('comment/<int:pk>/', CommentView.as_view({'delete': 'destroy'})),
    
]

