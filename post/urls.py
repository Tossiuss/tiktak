from django.urls import path
from .views import PostView,PostCategorySearchView
urlpatterns = [
    path('posts/create/', PostView.as_view({'post': 'create'})),
    path('posts/<int:pk>/', PostView.as_view({'delete': 'destroy','get':'retrieve'})),
    path('posts/',PostView.as_view({'get':'list'})),
    path('posts/search/',PostCategorySearchView.as_view())
]

