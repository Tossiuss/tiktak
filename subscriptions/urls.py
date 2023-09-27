from django.urls import path
from .views import SubscriptionCreateView, SubscriptionDeleteView, SubscriptionListView


urlpatterns = [
    path('subscriptions/', SubscriptionCreateView.as_view()),
    path('subscriptions/list/', SubscriptionListView.as_view()),  
    path('subscriptions/delete/<str:friend_email>/', SubscriptionDeleteView.as_view())
] 