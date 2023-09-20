from django.urls import path
from .views import PostView

urlpatterns = [
    path('new_post/', PostView.as_view({'post': 'create'})),
    path('list_post/', PostView.as_view({'get': 'list'})),
    path('retrieve_post/<int:pk>/', PostView.as_view({'get':'retrieve'})),
    path('del_post/<int:pk>/', PostView.as_view({'delete': 'destroy'})),
]

