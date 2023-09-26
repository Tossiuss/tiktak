# urls.py
from django.urls import path
from .views import LikeViewSet

urlpatterns = [
    path('api/v1/posts/<int:pk>/like/', LikeViewSet.as_view({'post': 'toggle_like'})),
]
