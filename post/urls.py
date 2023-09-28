from django.urls import path
from .views import PostView,PostCategorySearchView
urlpatterns = [
    path('api/v1/posts/create/', PostView.as_view({'post': 'create'})),
    path('api/v1/posts/<int:pk>/', PostView.as_view({'delete': 'destroy','get':'retrieve'})),
    path('api/v1/posts/',PostView.as_view({'get':'list'})),
    path('api/v1/posts/search/',PostCategorySearchView.as_view())
]

