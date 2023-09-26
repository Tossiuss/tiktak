from django.urls import path
from .views import PostView,PostCategorySearchView
urlpatterns = [
    path('posts/', PostView.as_view({'post': 'create','get':'list'})),
    path('posts/<int:pk>/', PostView.as_view({'delete': 'destroy','get':'retrieve'})),
    path('posts/search/',PostCategorySearchView.as_view())
]

